import matplotlib as mpl
import numpy as np

def colorFader(c1,c2,mix=0): 
    c1=np.array(mpl.colors.to_rgb(c1))
    c2=np.array(mpl.colors.to_rgb(c2))
    return mpl.colors.to_hex((1-mix)*c1 + mix*c2)

class EqTriTi(object):

    def __init__(self,Nr,Nc,L=1.):
        ysp = L/2.*np.tan(np.pi/6.)
        cnt = 0
        x = np.zeros((Nr,Nc))
        y = np.zeros((Nr,Nc))
        angs = np.zeros((Nr,Nc))
        row = 0
        r = 0
        while row < Nr:
            if cnt not in [2,5]:
                ty = ysp*float(r)
                cx = np.arange(0.,Nc*L,L)
                if cnt in [1,3]:
                    cx+=L/2.
                x[row] = cx
                y[row] = cx*0.+ty
                if cnt in [1,4]:
                    angs[row] = np.pi
                row += 1
            r += 1
            cnt+=1
            if cnt == 6: cnt = 0

        self.x = x.ravel()
        self.y = y.ravel()
        self.angs = angs.ravel()

class SimpleLine(object):

    def __init__(self,x1,x2,y1,y2):
        self.m = (y2-y1)/(x2-x1)
        self.b = y1-(self.m*x1)

    def get_y(self,x):
        return (self.m*x)+self.b

class SimpleCircle(object):

    def __init__(self,xc=0,yc=0,radius=1.,npoints=1000):

        self.r = radius
        self.cent = np.array([xc,yc])

        self.ang = np.linspace(0.,np.pi*2.,npoints)
        self.x = xc+(self.r*np.cos(self.ang))
        self.y = yc+(self.r*np.sin(self.ang))

class PowerFlower(object):

    def __init__(self,N=6,xs=0.,ys=0.,npoints=1000,rad=1.):

        self.xs = xs
        self.ys = ys
        self.N = N
        self.npoints = npoints
        self.rad=rad
        
        cent = SimpleCircle(xc=xs,yc=ys,npoints=self.npoints,radius=self.rad)
        self.angs = np.linspace(0,np.pi*2.,N+1)[:-1]
        self.xc,self.yc = np.cos(self.angs),np.sin(self.angs)
        self.layer = 0
        self.values = {f'layer{self.layer}':{'coords':np.vstack((rad*cent.x,rad*cent.y)),
                                             'cents':np.array([self.xc,self.yc])}
                      }

    def add_layer(self):
        
        self.layer+=1
        sc = self.rad*self.layer
        tx,ty = [],[]
        for i,ang in enumerate(self.angs):
            tx.append((self.rad*self.layer*self.xc[i])+self.xs)
            ty.append((self.rad*self.layer*self.yc[i])+self.ys)

            if self.layer > 1:
                try:
                    x1,x2 = (sc*self.xc[i])+self.xs,(sc*self.xc[i+1])+self.xs
                    y1,y2 = (sc*self.yc[i])+self.ys,(sc*self.yc[i+1])+self.ys
                    
                except:
                    x1,x2 = (sc*self.xc[i])+self.xs,(sc*self.xc[0])+self.xs
                    y1,y2 = (sc*self.yc[i])+self.ys,(sc*self.yc[0])+self.ys
                    
                if np.abs(x2-x1) >= 1.e-6:
                    tline = SimpleLine(x1,x2,y1,y2)
                    xs = np.linspace(x1,x2,self.layer+1)[1:-1]
                    ys = tline.get_y(xs)
                else:
                    xs = []
                    for i in range(self.layer-1): xs.append(x1)
                    ys = np.linspace(y2,y1,self.layer+1)[1:-1]
                for j in range(len(xs)):
                    tx.append(xs[j])
                    ty.append(ys[j])
        tmc = np.zeros((len(tx),2,self.npoints))
        for i in range(len(tx)):
            tcirc = SimpleCircle(xc=tx[i],yc=ty[i],npoints=self.npoints,radius=self.rad)
            tmc[i] = np.vstack((tcirc.x,tcirc.y))

            

        self.values[f'layer{self.layer}'] = {'coords':tmc}
        tx.append(tx[0])
        ty.append(ty[0])
        self.values[f'layer{self.layer}']['cents'] = np.vstack((tx,ty))
