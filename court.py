from tkinter import Canvas
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle, Arc
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np
import matplotlib.lines as lines


def drawCourt():
    img = plt.imread("images/basketball_court_background.jpg")
    color="black"
    lw=1
    zorder=1
#     fig = plt.figure(figsize=(9.4,6.0))
    #fig = Figure([9.4, 6.0])
    fig, ax = plt.subplots()
    im = ax.imshow(img, extent=[-50,50,-30,30])
    fig.set_figheight(5)
    fig.set_figwidth(8.4)
    # ax = plt.gca()
    # axmax  = fig.add_axes([0.25, 0.01, 0.65, 0.03])
        
    # Creates the out of bounds lines around the court
    outer = Rectangle((-47,-25), width=94, height=50, color=color, zorder=zorder, fill=False, lw=lw)
    ax.add_artist(lines.Line2D([-47, 47],[-25, -25], color=color, zorder=zorder, lw=lw))
    ax.add_artist(lines.Line2D([-47, 47],[25, 25], color=color, zorder=zorder, lw=lw))
    ax.add_artist(lines.Line2D([-47, -47],[-25, 25], color=color, zorder=zorder, lw=lw))
    ax.add_artist(lines.Line2D([0,0],[1,1], color=color, zorder=zorder, lw=lw))
    
    # Creates the center circles and center line
    center_circle = Circle((0, 0), radius=6, lw=lw, fill=False,
                           color=color, zorder=zorder)

    # Center line
    ax.add_artist(lines.Line2D([0,0],[25,-25], color=color, zorder=zorder, lw=lw))
    
    # The four dash lines near the middle of the court (Idk what they are called)
    ax.add_artist(lines.Line2D([-19,-19],[-22,-25], color=color, zorder=zorder, lw=lw))
    ax.add_artist(lines.Line2D([19,19],[-22,-25], color=color, zorder=zorder, lw=lw))
    ax.add_artist(lines.Line2D([-19,-19],[22,25], color=color, zorder=zorder, lw=lw))
    ax.add_artist(lines.Line2D([19,19],[22,25], color=color, zorder=zorder, lw=lw))
    
     # Left and right paint areas
    l_box = Rectangle((-47, -6), 19, 12, lw=lw, fill=False,
                            color=color, zorder=zorder)
    r_box = Rectangle((28, -6), 19, 12, lw=lw, fill=False,
                            color=color, zorder=zorder)
    
    # Left and right free throw circles
    l_free_throw_fill = Arc((-28,0), 12, 12, theta1=270, theta2=90, lw=lw, fill=False,
                          color=color, zorder=zorder)
    r_free_throw_fill = Arc((28,0), 12, 12, theta1=90, theta2=270, lw=lw, fill=False,
                          color=color, zorder=zorder)
    l_free_throw_dash = Arc((-28,0), 12, 12, theta1=90, theta2=270, lw=lw, fill=False, color=color,
                            zorder=zorder, linestyle='dashed')
    r_free_throw_dash = Arc((28,0), 12, 12, theta1=270, theta2=90, lw=lw, fill=False, color=color,
                            zorder=zorder, linestyle='dashed')
    
    # Restricted Areas
    l_restricted_arc = Arc((-41.75,0), 6, 6, theta1=260, theta2=100, lw=lw, fill=False, color=color, zorder=zorder)
    r_restricted_arc = Arc((41.75,0), 6, 6, theta1=80, theta2=280, lw=lw, fill=False, color=color, zorder=zorder)
    
    # Backboard
    ax.add_artist(lines.Line2D([-43,-43],[3,-3], color=color, zorder=zorder, lw=lw))
    ax.add_artist(lines.Line2D([43,43],[-3,3], color=color, zorder=zorder, lw=lw))
    
    # Hoop
    l_hoop = Circle((-41.75,0), radius=0.75, lw=1, fill=False, 
                    color=color, zorder=zorder)
    r_hoop = Circle((41.75,0), radius=0.75, lw=1, fill=False,
                    color=color, zorder=zorder)
    
    # Straight part of corner 3pt lines (4 total)
    ax.add_artist(lines.Line2D([-47,-41.75],[-20.70,-20.70], color=color, zorder=zorder, lw=lw))
    ax.add_artist(lines.Line2D([-47,-41.75],[20.75,20.75], color=color, zorder=zorder, lw=lw))
    ax.add_artist(lines.Line2D([47,41.75],[-20.70,-20.70], color=color, zorder=zorder, lw=lw))
    ax.add_artist(lines.Line2D([47,41.75],[20.75,20.75], color=color, zorder=zorder, lw=lw))
    
    # 3pt Arc
    l_arc = Arc((-41.75,0), 41.5, 41.5, theta1=270, theta2=90, lw=lw,
                color=color, zorder=zorder)
    r_arc = Arc((41.75,0), 41.5, 41.5, theta1=90, theta2=270, lw=lw,
                color=color, zorder=zorder)
    
    # Extra Lines
    top_left_rect = Rectangle((-40,6), 1, 0.7, lw=lw, fill=True, color=color, zorder=zorder)
    bottom_left_rect = Rectangle((-40,-6.7), 1, 0.7, lw=lw, fill=True, color=color, zorder=zorder)
    top_right_rect = Rectangle((39,6), 1, 0.7, lw=lw, fill=True, color=color, zorder=zorder)
    bottom_right_rect = Rectangle((39,-6.7), 1, 0.7, lw=lw, fill=True, color=color, zorder=zorder)
    ax.add_artist(lines.Line2D([-36,-36],[6,6.7], color=color, zorder=zorder, lw=lw))
    ax.add_artist(lines.Line2D([36,36],[6,6.7], color=color, zorder=zorder, lw=lw))
    ax.add_artist(lines.Line2D([-36,-36],[-6,-6.7], color=color, zorder=zorder, lw=lw))
    ax.add_artist(lines.Line2D([36,36],[-6,-6.7], color=color, zorder=zorder, lw=lw))
    ax.add_artist(lines.Line2D([-33,-33],[6,6.7], color=color, zorder=zorder, lw=lw))
    ax.add_artist(lines.Line2D([33,33],[6,6.7], color=color, zorder=zorder, lw=lw))
    ax.add_artist(lines.Line2D([-33,-33],[-6,-6.7], color=color, zorder=zorder, lw=lw))
    ax.add_artist(lines.Line2D([33,33],[-6,-6.7], color=color, zorder=zorder, lw=lw))
    ax.add_artist(lines.Line2D([-30,-30],[6,6.7], color=color, zorder=zorder, lw=lw))
    ax.add_artist(lines.Line2D([30,30],[6,6.7], color=color, zorder=zorder, lw=lw))
    ax.add_artist(lines.Line2D([-30,-30],[-6,-6.7], color=color, zorder=zorder, lw=lw))
    ax.add_artist(lines.Line2D([30,30],[-6,-6.7], color=color, zorder=zorder, lw=lw))
    
    
    court_elements = [outer, center_circle, l_box, r_box, l_free_throw_fill, r_free_throw_fill, l_free_throw_dash, 
                      r_free_throw_dash, l_hoop, r_hoop, l_arc, r_arc, l_restricted_arc, r_restricted_arc, top_left_rect, 
                      bottom_left_rect, top_right_rect, bottom_right_rect]

    # Add the court elements onto the axes
    for element in court_elements:
        ax.add_patch(element)

    plt.axis('off')
    plt.xlim([-48,48])
    plt.ylim([-26,26])
    plt.tight_layout()
    return fig, ax