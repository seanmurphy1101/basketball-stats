import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle, Arc, Wedge
from matplotlib.lines import Line2D
import pandas as pd
import numpy as np
from PIL import Image
from shapely.geometry import Point, Polygon
import math

def draw_court_vertical(color="black", lw=2, zorder=1):
    img = Image.open("images/basketball_court_background.jpg")
    img = img.rotate(90, expand=True)
    
    fig=plt.figure(figsize=(12.0,10.0))
    ax=fig.add_subplot(1,1,1)
    im = ax.imshow(img, extent=[-30,30,-5,50])
    ax = plt.gca()
        
    # Creates the out of bounds lines around the half court
    outer = Rectangle((-25,0), width=50, height=47, color=color,
                      zorder=zorder, fill=False, lw=lw)
    
    # Creates the center circles and center line
    center_circle = Circle((0, 0), radius=6, lw=lw, fill=False,
                           color=color, zorder=zorder)

    # Center line
    ax.plot([-25,25],[0,0], color=color, zorder=zorder, lw=lw)
    
    # The dash lines near the middle of the court (Idk what they are called)
    ax.plot([-25,-22],[19,19], color=color, zorder=zorder, lw=lw)
    ax.plot([22,25],[19,19], color=color, zorder=zorder, lw=lw)
    
    # Paint Area
    box = Rectangle((-6, 28), 12, 19, lw=lw, fill=False,
                            color=color, zorder=zorder)
    
    # Left and right free throw circles
    free_throw_fill = Arc((0,28), 12, 12, theta1=180, theta2=360, lw=lw, fill=False,
                          color=color, zorder=zorder)
    free_throw_dash = Arc((0,28), 12, 12, theta1=0, theta2=180, lw=lw, fill=False, color=color,
                            zorder=zorder, linestyle='dashed')
    
    # Backboard
    ax.plot([3,-3],[43,43], color=color, zorder=zorder, lw=1)
    
    # Hoop
    hoop = Circle((0,41.75), radius=0.75, lw=1, fill=False, 
                    color=color, zorder=zorder)
    
    # Straight part of corner 3pt lines
    ax.plot([-19.75,-19.75],[47,41.75], color=color, zorder=zorder, lw=lw)
    ax.plot([19.75,19.75],[47,41.75], color=color, zorder=zorder, lw=lw)
    
    # 3pt Arc
    arc = Arc((0,41.75), 39.5, 39.5, theta1=180, theta2=360, lw=lw,
                color=color, zorder=zorder)
    
    # Extra Lines
    top_rect = Rectangle((6,40), 0.7, 1, lw=lw, fill=True, color=color, zorder=zorder)
    bottom_rect = Rectangle((-6.7,40), 0.7, 1, lw=lw, fill=True, color=color, zorder=zorder)
    ax.plot([6,6.7],[36,36], color=color, zorder=zorder, lw=lw)
    ax.plot([-6,-6.7],[36,36], color=color, zorder=zorder, lw=lw)
    ax.plot([6,6.7],[33,33], color=color, zorder=zorder, lw=lw)
    ax.plot([-6,-6.7],[33,33], color=color, zorder=zorder, lw=lw)
    ax.plot([6,6.7],[30,30], color=color, zorder=zorder, lw=lw)
    ax.plot([-6,-6.7],[30,30], color=color, zorder=zorder, lw=lw)
    
    
    court_elements = [outer, center_circle, box, free_throw_fill, free_throw_dash, hoop, arc, top_rect, bottom_rect]

    # Add the court elements onto the axes
    for element in court_elements:
        ax.add_patch(element)
        
    legend_elements = [Line2D([0],[0], marker='o', color='w', label='Made Shot', markerfacecolor='green', markersize=12),
                      Line2D([0],[0], marker='o', color='w', label='Missed Shot', markerfacecolor='red', markersize=12)]

    plt.axis('off')
    plt.suptitle('Shot Chart Example', fontsize=25, color='white')
    ax.legend(handles=legend_elements, loc='best')
    plt.xlim([-26,26])
    plt.ylim([0,47])
    plt.tight_layout()
    return fig, ax

def map_shots(df, name, file_path):
    fig, ax = draw_court_vertical()
    for index, shots in df.iterrows():
        if shots.missed == True:
            shot_color = 'red'
        else:
            shot_color = 'green'
            
        circle = plt.Circle((-(shots.y), (shots.x)), 0.5, color=shot_color)
        ax.add_artist(circle)
        plt.draw()
        
    plt.savefig(f'{file_path}{name}_shot_chart.png', bbox_inches='tight')
    plt.close()
#     plt.show()