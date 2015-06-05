import pickle
f=open('a_w_v.p','rb');#this file is uploaded in Longform folder
a_f=pickle.load(f);
f.close();
f=open('dictionary.p','rb');
d=pickle.load(f);
f.close()
score=[];
st=0.5;
ed=0.5;
for i in range(0,len(d)):
	l=[];
	for item in a_f[1:-1]:
		l.append( (1.0/len(d)-(st*abs(item[i]-a_f[0][i])+ed*abs(item[i]-a_f[-1][i])))/(1.0/len(d)));
	score.append(l);
