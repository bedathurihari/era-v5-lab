"""Small deterministic causal decoder with real top-1 MoE per token (synthetic data)."""
import argparse,json,math,random,time
from pathlib import Path
import numpy as np,torch,torch.nn as nn,torch.nn.functional as F,yaml

class Block(nn.Module):
    def __init__(self,d,h,e):
        super().__init__();self.norm1=nn.LayerNorm(d);self.attn=nn.MultiheadAttention(d,h,batch_first=True,dropout=0.0)
        self.norm2=nn.LayerNorm(d);self.router=nn.Linear(d,e)
        self.experts=nn.ModuleList([nn.Sequential(nn.Linear(d,2*d),nn.GELU(),nn.Linear(2*d,d)) for _ in range(e)])
    def forward(self,x):
        T=x.shape[1];mask=torch.ones(T,T,device=x.device,dtype=torch.bool).triu(1)
        z=self.norm1(x);x=x+self.attn(z,z,z,attn_mask=mask,need_weights=False)[0]
        z=self.norm2(x);route=self.router(z);idx=route.argmax(-1)
        # Computation is sparse: each token goes through its selected expert only.
        flat=z.reshape(-1,z.shape[-1]);chosen=idx.reshape(-1);out=torch.zeros_like(flat)
        for j,expert in enumerate(self.experts):
            ids=(chosen==j).nonzero(as_tuple=True)[0]
            if ids.numel():out=out.index_copy(0,ids,expert(flat.index_select(0,ids)))
        return x+out.reshape_as(x)
class TinyMoE(nn.Module):
    def __init__(self,c):
        super().__init__();d=c['hidden_size'];self.emb=nn.Embedding(c['vocab_size'],d);self.pos=nn.Embedding(c['seq_len'],d)
        self.blocks=nn.ModuleList([Block(d,c['num_heads'],c['num_experts']) for _ in range(c['num_layers'])]);self.norm=nn.LayerNorm(d);self.head=nn.Linear(d,c['vocab_size'])
    def forward(self,x):
        h=self.emb(x)+self.pos(torch.arange(x.shape[1],device=x.device))
        for b in self.blocks:h=b(h)
        return self.head(self.norm(h))
def run(config,output):
    c=yaml.safe_load(Path(config).read_text());seed=c['seed'];random.seed(seed);np.random.seed(seed);torch.manual_seed(seed);torch.set_num_threads(1)
    torch.use_deterministic_algorithms(True)
    device='cpu'  # Gate 1 CPU deterministic reference; separate GPU run must be rechecked
    model=TinyMoE(c).to(device);opt=torch.optim.AdamW(model.parameters(),lr=c['lr']);logs=[]
    for step in range(c['steps']):
        # Frozen synthetic pattern: next token is (previous token + 1) modulo vocab.
        start=torch.arange(c['batch_size']).unsqueeze(1);offset=torch.arange(c['seq_len']+1).unsqueeze(0)
        batch=(start+offset)%c['vocab_size'];x=batch[:,:-1].to(device);y=batch[:,1:].to(device)
        t0=time.perf_counter();opt.zero_grad(set_to_none=True);logits=model(x)
        loss=F.cross_entropy(logits.reshape(-1,c['vocab_size']),y.reshape(-1));
        if not torch.isfinite(loss):raise RuntimeError(f'Nonfinite loss at step {step}')
        loss.backward();opt.step();duration=max(time.perf_counter()-t0,1e-9)
        logs.append({'step':step,'loss':round(loss.item(),9),'loss_ntp':round(loss.item(),9),'loss_mtp':None,
            'lr':c['lr'],'tokens_per_second':round(y.numel()/duration,1),'gpu_alloc_gb':None})
    if output:
        Path(output).parent.mkdir(parents=True,exist_ok=True);Path(output).write_text('\n'.join(json.dumps(r,sort_keys=True) for r in logs)+'\n')
    print(f"steps={len(logs)} first={logs[0]['loss']:.6f} last={logs[-1]['loss']:.6f} finite=all")
    return logs
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--config',default=str(Path(__file__).resolve().parents[1]/'configs/config_tiny.yaml'));ap.add_argument('--output');args=ap.parse_args();run(args.config,args.output)
