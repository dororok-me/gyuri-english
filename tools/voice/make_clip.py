"""규리 대사 → 녹음(mp3 data URI) + 단어 시간 + 입모양 키 + 음량 (index.html CLIPS 형식)
목소리: Kokoro af_heart, 속도 0.85, 음 높이 1.25배 (원래 규리 목소리와 맞춘 값)"""
import sys,os,json,re,base64,subprocess,wave,numpy as np,soundfile as sf
from kokoro_onnx import Kokoro
from vosk import Model,KaldiRecognizer,SetLogLevel
from phonemizer.backend.espeak.wrapper import EspeakWrapper
import espeakng_loader
EspeakWrapper.set_library(espeakng_loader.get_library_path()); EspeakWrapper.set_data_path(espeakng_loader.get_data_path())
from phonemizer import phonemize
SetLogLevel(-1)
S=sys.argv[1]; OUT=f'{S}/clips'; os.makedirs(OUT,exist_ok=True)
VOICE,SPEED,PITCH='af_heart',0.85,1.25
K=Kokoro(f'{S}/kok/model_q8.onnx',f'{S}/kok/voices.npz')
VM=Model(f'{S}/vmodel/'+[d for d in os.listdir(f'{S}/vmodel') if not d.startswith('.')][0]) if not os.path.exists(f'{S}/vmodel/am') else Model(f'{S}/vmodel')
def ff(*a): subprocess.run(['ffmpeg','-loglevel','error','-y',*a],check=True)
V={'p':'MBP','b':'MBP','m':'MBP','f':'FV','v':'FV','θ':'DD','ð':'DD','t':'DD','d':'DD','n':'DD','l':'DD','ɾ':'DD','k':'KK','ɡ':'KK','g':'KK','ŋ':'KK','h':'KK',
   's':'SS','z':'SS','ʃ':'SH','ʒ':'SH','ɹ':'R','r':'R','w':'U','j':'E',
   'a':'AA','ɑ':'AA','ɐ':'AA','æ':'AA','ʌ':'AA','ə':'AA','ɚ':'R','ɜ':'R','e':'E','ɛ':'E','ɪ':'E','i':'E','ᵻ':'E','o':'O','ɔ':'O','u':'U','ʊ':'U'}
VOW=set('aɑɐæʌəɚɜeɛɪiᵻoɔuʊ')
def visemes(word):
    ph=phonemize([word],language='en-us',backend='espeak',strip=True,with_stress=False)[0]
    ph=ph.replace('tʃ','ʃ').replace('dʒ','ʃ').replace('ː','')
    out=[]
    for ch in ph:
        v=V.get(ch)
        if not v: continue
        w=2 if ch in VOW else 1
        if out and out[-1][0]==v: out[-1][1]+=w
        else: out.append([v,w])
    return out or [['AA',1]]
def make(cid,text):
    a,sr=K.create(text,voice=VOICE,speed=SPEED,lang='en-us')
    raw=f'{OUT}/{cid}_raw.wav'; sf.write(raw,a,sr)
    sh=f'{OUT}/{cid}_sh.wav'; ff('-i',raw,'-af',f'asetrate={int(24000*PITCH)},aresample=24000,atempo={1/PITCH:.5f}',sh)
    x,_=sf.read(sh); x=x.astype(np.float32)
    idx=np.where(np.abs(x)>0.01)[0]; st=max(0,idx[0]-int(0.02*24000)); en=min(len(x),idx[-1]+int(0.25*24000))
    x=x[st:en]; fin=f'{OUT}/{cid}.wav'; sf.write(fin,x,24000)
    mp3=f'{OUT}/{cid}.mp3'; ff('-i',fin,'-ac','1','-ar','24000','-b:a','48k',mp3)
    dur=round(len(x)/24000,3)
    # 단어 시간: Vosk로 맞춤 (단어 목록을 이 문장 단어로 좁힘)
    toks=text.split(); words=[re.sub(r"[^a-z']",'',t.lower()) for t in toks]
    w16=f'{OUT}/{cid}_16.wav'; ff('-i',fin,'-ac','1','-ar','16000','-sample_fmt','s16',w16)
    rec=KaldiRecognizer(VM,16000,json.dumps(sorted(set(w.replace("'",'') for w in words))+['[unk]'])); rec.SetWords(True)
    with wave.open(w16) as wf:
        while True:
            b=wf.readframes(4000)
            if not b: break
            rec.AcceptWaveform(b)
    got=[w for w in json.loads(rec.FinalResult()).get('result',[])]
    if [g['word'] for g in got]==[w.replace("'",'') for w in words]:
        times=[[g['start'],g['end']] for g in got]; how='vosk'
    else: # 못 맞추면 소리 나는 구간을 글자 수 비율로 나눔
        v0=idx[0]/24000-st/24000; v1=(idx[-1]-st)/24000; L=sum(len(w) for w in words); t=v0; times=[]
        for w in words: d=(v1-v0)*len(w)/L; times.append([t,t+d]); t+=d
        how='even'
    wlist=[[tok,round(float(s),3),round(float(e),3)] for tok,(s,e) in zip(toks,times)]
    keys=[]
    for i,(tok,s,e) in enumerate(wlist):
        vs=visemes(re.sub(r"[^A-Za-z' -]",'',tok)); W=sum(w for _,w in vs); t=s
        for v,w in vs: keys.append([round(t,3),v]); t+=(e-s)*w/W
        nxt=wlist[i+1][1] if i+1<len(wlist) else None
        if nxt is None or nxt-e>0.15: keys.append([round(e,3),'REST'])
    if keys[-1][1]=='MBP': pass
    fr=0.02; n=int(np.ceil(dur/fr))+1; hop=int(24000*fr)
    env=np.array([np.sqrt(np.mean(x[i*hop:(i+1)*hop]**2)) if i*hop<len(x) else 0 for i in range(n)])
    env=np.round(env/env.max(),2).tolist()
    clip={'ch':'A','text':text,'dur':dur,'fr':fr,'env':env,'keys':keys,'words':wlist,
          'audio':'data:audio/mpeg;base64,'+base64.b64encode(open(mp3,'rb').read()).decode()}
    return clip,how
if __name__=='__main__':
    lines=json.load(open(sys.argv[2]))
    res={}
    for cid,text in lines.items():
        c,how=make(cid,text); res[cid]=c; print(cid,how,c['dur'],c['words'])
    json.dump(res,open(f'{OUT}/clips.json','w'))
