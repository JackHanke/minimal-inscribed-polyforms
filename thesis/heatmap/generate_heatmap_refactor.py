from numpy import zeros, amax, ndarray
from math import comb, ceil
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
from matplotlib import colors, cm

# returns unscaled heat value
def heat(h: int, w: int, i: int, j:int) -> int:
    if i == 1 and j == 1: return (2*comb(h+w-2,h-1) - 1)
    if i == 1: return (2*comb(w + h-j,w-1) + 2*comb(w+ j-1, w-1) - 3*w)
    if j == 1: return (2*comb(w-i + h,h-1) + 2*comb(i-1 + h, h-1) - 3*h)
    else: 
        return ((2*comb(i+j-2,i-1)-1) * (2*comb(w-i+h-j,w-i)-1) + \
                (2*comb(i-1+h-j,i-1)-1) * (2*comb(w-i+j-1,w-i)-1) + \
                2*comb(w-i+h-j,h-j-1)+ 2*comb(w-i+h-j,w-i-1)+ 2*comb(i+j-2,j-2)+ 2*comb(i+j-2,i-2) + \
                2*comb(i-1+h-j,h-j-1)+ 2*comb(i-1+h-j,i-2)+ 2*comb(w-i+j-1,j-2)+ 2*comb(w-i+j-1,w-i-1) - \
                (3*(h+w-2)) -1)

# creates map with scaled heat
def make_map(h: int, w: int) -> ndarray:
    return_array = zeros((h, w))
    total = 8*comb(h+w-2, h-1) - 3*h*w + 2*h + 2*w - 8

    # interior
    for i in range(1, ceil(w/2)+1):
        for j in range(1, ceil(h/2)+1):
            # calculate and scale heat
            heat_val = heat(h, w, i, j) / total
            # set heat vals         
            return_array[j-1][i-1] = heat_val
            return_array[h-j][i-1] = heat_val
            return_array[j-1][w-i] = heat_val
            return_array[h-j][w-i] = heat_val
    return return_array

# creates animation
def create_anim(n: int) -> FuncAnimation:
    # set up the first frame
    data = make_map(1, 1)
    fig, ax = plt.subplots()
    im = ax.imshow(data)
    im.set_cmap(cm.plasma)
    ax.tick_params(top=False, bottom=False, left=False, right=False,labelleft=False, labelbottom=False)
    ax.set_title(f'{1} x {1} Heatmap')
    colorbar = fig.colorbar(im, ticks = [0,amax(data)])

    def animate(t: int):
        #setting up all subsequent frames
        ax.set_title(f"{t+1} x {t+1} Heatmap")
        #set data, data norm, and data colormap
        data = make_map(t+1, t+1)
        #refresh colorbar
        colorbar.set_ticks([0,amax(data)])
        im.set_data(A=data)
        norm = colors.Normalize(vmin=0, vmax=amax(data)) # replace vmax with 1 to not scale coloring
        im.set_norm(norm)
        cmap = cm.plasma
        im.set_cmap(cmap)
        return im,

    anim = FuncAnimation(fig, animate, frames = n, blit = True)
    return anim

anim = create_anim(100) 
anim.save(r"./heatmap.gif", writer=PillowWriter(fps=30))