import numpy

def zai(points, polygon, append = -2): #'in'
    if polygon == 'random':
        #make a random polygon! (for testing) 
        n = 5
        #random points
        px = (np.random.rand(n))
        py = (np.random.rand(n))
        #scale them to data
        pxm,pxM = self.df.x.min(),self.df.x.max()
        pym,pyM = self.df.y.min(),self.df.y.max()
        px = px*(pxM-pxm)+pxm
        py = py*(pyM-pym)+pym
        #make into polygon (add first point to end)
        px = np.concatenate((px, np.array([px[0]])))
        py = np.concatenate((py, np.array([py[0]])))
        polygon = px,py
        polygon = np.asarray(polygon)
        polygon = polygon.T
        # print polygon
        # raw_input('random polygon ok?')
    
    n = self.df.x.size
    vert = polygon.shape[0]-1
    # print 'shape', polygon.shape
    # raw_input('is this ok?')
    wn = self.df.x*0
    for i in range(0,vert):
        P0,P1 = polygon[i], polygon[i+1]
        print(P0, P1)
        pgon = polygon[i:i+2].T[1]
        st = np.argsort(pgon)

        left = (((P1[0]-P0[0])*(self.df.y-P0[1])-(self.df.x-P0[0])*(P1[1]-P0[1]))<0)
        strip = np.logical_and(self.df.y>=pgon[st[0]], self.df.y<pgon[st[1]])

        if st[0]:
            print('purple minus',st)
            wn -= ~left&strip
        else:
            print('green plus',st)
            wn += left&strip

    #could just put out the winding number
    # self.df['wn']=wn

    # idx=idx.astype('bool')

    if append == -2:
        # print(idx.dtype)
        idx  = wn!=0
        return idx

    #todo list
    return self

def gong(self, val, agg, scale, where =1, x='x', y='y', aggmode = 'np'): #	just, honorable (designation), public, common
    #rewriting of quickgrid

    # print('SUM',where.max())

    x = self.df[x].values
    y = self.df[y].values
    z = self.df[val].values

    #preprep
    x = x - x.min()
    y = y - y.min()
    y = y.max()-y
    # x = x.max()-x

    

    dx = int(math.ceil(x.max()-x.min()))
    dy = int(math.ceil(y.max()-y.min()))

    print('x range', x.min(), x.max(),x.max()-x.min())
    print('y range', y.min(), y.max(),y.max()-y.min()) 

    #scale
    scale = 1/float(scale)
    x*=scale
    y*=scale
    dx=int(math.ceil(dx*scale))
    dy=int(math.ceil(dy*scale))
    x+=1

    print('grid',dx,dy)
    print('gridsize',dx*dy)

    #make empty 1d grid
    g1d = np.zeros((dx*dy))
    g1d[:] = np.nan

    #reduce the point set down - bit of a hack
    #could certainly load the smallsubset from the df first and do the extents calculation on df max/min
    if hasattr(where, "__len__"):
        x = x[where]
        y = y[where]
        z = z[where]

    #res data 1d, sort
    xy = y.astype(int)*dx+x.astype(int)-1
    xysorter = xy.argsort()
    xys = xy[xysorter]
    zs = z[xysorter]

    #find the cells
    xyr = (xys-np.roll(xys, 1)).astype(bool)
    xyrb = np.where(xyr>0)[0]

    print('max hashIndex', xys.max())


    #iterate over points
    for i in range(0,xyrb.size-1):
        gindex1d =  xys[xyrb[i]]
        # zVal = zs[xyrb[i]:xyrb[i+1]].max()
        if aggmode == 'np':
            zVal = getattr(np,agg)(zs[xyrb[i]:xyrb[i+1]])
        elif aggmode == 'scipy':
            zVal = getattr(stats,agg)(zs[xyrb[i]:xyrb[i+1]])[0] #TODO the zero slice is because mode in scipy returns the value and the count, horrible code here
        # g1d[gindex1d] = zVal
        try:
            g1d[gindex1d] = zVal
        except:
            pass
    ##awkward way of getting the last cell in the array, should be done smoother in the loop...
    ## TODO fix this awkward step
    try:
        gindex1d =  xys[xyrb[-1]]
        if aggmode == 'np':
                zVal = getattr(np,agg)(zs[xyrb[-1]:])
        elif aggmode == 'scipy':
                zVal = getattr(stats,agg)(zs[xyrb[-1]:])[0]
        g1d[gindex1d] = zVal
    except: 
        pass # in certain instances this fails. I believe it is when grids are 0 dimension. TODO maoek robust

    #reshape the grid into 2d
    g2d = g1d.reshape((dy, dx),order='C')
    return g2d

def zi(a, b): #	child, son
    return (a-b)/(a+b)

def sheng(qi=0.0, shu = 1, er=0): #to be born, to give birth, life, to grow
    if isinstance(qi,int):
        return numpy.random.randint(er,qi+1, shu)
    else:
        return numpy.random.rand(shu)

def ding(): #to set, to fix, to determine, to decide, to order
    '''apply a filter, resucing array size'''
    pass

def jian(qi): #to see, to meet, to appear (to be something), to interview / appear
    ''' display data to the screen'''
    print(qi)
    pass

def biao(): #'whirlwind
    'normalize difference ratio'
    pass

def nian(): #'twist'
    pass

def fangsha(): #'spinning'
    pass

if __name__ == '__main__':
    import numpy

    sigma_circle(polygon = 'random')