from numpy import zeros, amax
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
from matplotlib import colors
from matplotlib import cm
from math import comb, ceil

def make_data(w,l):
    #notice the switch and direction of the array, ie. return_array[j][i]
    return_array = zeros((l,w))
    total_val = 8*comb(l+w-2,l-1) - 3*l*w + 2*l + 2*w - 8
    #total_val = 1

    #corners
    corner_val = (2*comb(l+w-2,l-1) - 1)/total_val
    return_array[0][0] = corner_val
    return_array[l-1][0] = corner_val
    return_array[0][w-1] = corner_val
    return_array[l-1][w-1] = corner_val

    #edges
    for i in range(2,ceil(w/2)+1):
        edge_value = (2*comb(w-i + l,l-1) + 2*comb(i-1 + l, l-1) - 3*l)/total_val
        return_array[0][i-1] = edge_value
        return_array[0][w-i] = edge_value
        return_array[l-1][i-1] = edge_value
        return_array[l-1][w-i] = edge_value

    for j in range(2,ceil(l/2)+1):
        edge_value = (2*comb(w + l-j,w-1) + 2*comb(w+ j-1, w-1) - 3*w)/total_val
        return_array[j-1][0] = edge_value
        return_array[l-j][0] = edge_value
        return_array[j-1][w-1] = edge_value
        return_array[l-j][w-1] = edge_value

    # interior
    for i in range(2, ceil(w/2)+1):
        for j in range(2, ceil(l/2)+1):
            interior_value = ((2*comb(i+j-2,i-1)-1) * (2*comb(w-i+l-j,w-i)-1) + \
                (2*comb(i-1+l-j,i-1)-1)*(2*comb(w-i+j-1,w-i)-1) + \
                2*comb(w-i+l-j,l-j-1)+ 2*comb(w-i+l-j,w-i-1)+ 2*comb(i+j-2,j-2)+ 2*comb(i+j-2,i-2) + \
                2*comb(i-1+l-j,l-j-1)+ 2*comb(i-1+l-j,i-2)+ 2*comb(w-i+j-1,j-2)+ 2*comb(w-i+j-1,w-i-1) - \
                (3*(l+w-2)) -1)/total_val

            return_array[j-1][i-1] = interior_value
            return_array[l-j][i-1] = interior_value
            return_array[j-1][w-i] = interior_value
            return_array[l-j][w-i] = interior_value

    return return_array

def create_video(n):
    #setting up first frame
    data = make_data(2,2)
    fig, ax = plt.subplots()
    im = ax.imshow(data)
    im.set_cmap(cm.plasma)
    ax.tick_params(top=False, bottom=False, left=False, right=False,labelleft=False, labelbottom=False)
    ax.set_title('{} x {} Heatmap'.format(1,1))

    colorbar = fig.colorbar(im, ticks = [0,amax(data)])

    def animate(t):
        #setting up all subsequent frames
        global data

        data = make_data(t+2,t+2)
        cmap = cm.plasma
        norm = colors.Normalize(vmin=0, vmax=amax(data)) #can replace vmax with 1 if I dont want the colors to scale
        #norm = colors.Normalize(vmin=0, vmax=1)

        ax.set_title('{} x {} Heatmap'.format(t+2,t+2))

        #refresh colorbar
        colorbar.set_ticks([0,amax(data)])

        #set data, data norm, and data colormap
        im.set_data(A=data)
        im.set_norm(norm)
        im.set_cmap(cmap)
        return im, 

    anim = FuncAnimation(fig, animate, frames = n, interval = 450, blit = True)
    plt.show()

    return anim

anim = create_video(130)

#print(make_data(2,5))

save = False
if save:
    f = r"/Users/jeffreyhanke/Desktop/TheVault/Projects/Minimals/heatmap.gif" 
    writergif = PillowWriter(fps=30) 
    anim.save(f, writer=writergif)
    print('Save successful.')

#tests to see when the near-corner point 1,1 surpasses the center as being the highest density cell (it's 15)
test = False
if test:
    n=2
    done = False
    while not done:
        array = make_data((2*n)+1,(2*n)+1)
        if array[1][1] > array[n][n]:
            print('n is',n)
            print('(2,2) is {} and (n+1,n+1) is {}'.format(array[1][1], array[n][n]))
            print(array)
            done = True
        else:
            n += 1

test2 = False
if test2:
    for n in range(5,40):
        i=2
        j=2
        w=n
        l=n
        total_val = 8*comb(l+w-2,l-1) - 3*l*w + 2*l + 2*w - 8
        interior_value = ((2*comb(i+j-2,i-1)-1) * (2*comb(w-i+l-j,w-i)-1) + \
                    (2*comb(i-1+l-j,i-1)-1)*(2*comb(w-i+j-1,w-i)-1) + \
                    2*comb(w-i+l-j,l-j-1)+ 2*comb(w-i+l-j,w-i-1)+\
                    2*comb(i+j-2,j-2)+ 2*comb(i+j-2,i-2) + \
                    2*comb(i-1+l-j,l-j-1)+ 2*comb(i-1+l-j,i-2)+ 2*comb(w-i+j-1,j-2)+ 2*comb(w-i+j-1,w-i-1) - \
                    (3*(l+w-2)) -1)/total_val

        print('a[1][1] for n={} is {}'.format(n,interior_value))


