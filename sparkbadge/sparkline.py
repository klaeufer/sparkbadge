from typing import List, Tuple
import drawsvg as draw
import numpy as np
# For testing purposes
import tempfile
import webbrowser

HEIGHT = 13
WIDTH = 107
X_OFFSET = 7
Y_OFFSET = 1

def normalize(arr: np.ndarray) -> np.ndarray:
    max_arr = np.max(arr)
    if max_arr != 0:
        arr /= max_arr
    return arr


def fit_data(samples: List[int]) -> Tuple[List[int], List[int]]:
    width = WIDTH - X_OFFSET
    N = int(width / len(samples))
    y = np.repeat(samples, N)
    xp = np.linspace(start=X_OFFSET, stop=width, num=len(y))
    yp = normalize(np.poly1d(np.polyfit(xp, y, 15))(xp))
    yp *= (HEIGHT // 2 + 1)
    return xp.tolist(), yp.tolist()


def hist_trend(samples: List[int], stroke_color: str, stroke_width: int) -> str:
    canvas = draw.Drawing(WIDTH, HEIGHT, origin=(0, Y_OFFSET))

    xp, yp = fit_data(samples)

    for x, y in zip(xp, yp):
        fill = '#123456'
        if y >= 0:
            fill = 'green'
            y1 = HEIGHT // 2
            y2 = y
        else:
            fill = 'red'
            y1 = HEIGHT // 2 + y
            y2 = HEIGHT // 2 - y1

        rect = draw.Rectangle(x, y1, WIDTH // len(yp), y2, fill=fill)
        canvas.append(rect)

    canvas.append(
        draw.Line(WIDTH,
                  HEIGHT // 2,
                  0,
                  HEIGHT // 2,
                  stroke='white',
                  stroke_width=0.5,
                  fill='none'))

    #return canvas.asDataUri()
    return canvas.as_svg()


def trend(samples: List[int], stroke_color: str, stroke_width: int) -> str or None:
    canvas = draw.Drawing(WIDTH, HEIGHT, origin=(0, -Y_OFFSET))
    path = draw.Path(
        fill="transparent",
        stroke=stroke_color,
        stroke_width=stroke_width,
        stroke_linejoin="round",
    )

    xp, yp = fit_data(samples)
    path.M(xp[0], yp[0])
    for x, y in zip(xp[1:], yp[1:]):
        path.L(x, y)
    canvas.append(path)
    
    #return canvas.asDataUri()
    return canvas.as_svg()


def stacked_bar(samples, labels):
    #canvas = draw.Drawing(WIDTH, HEIGHT, origin=(0, Y_OFFSET))
    #canvas = draw.Drawing(200, 100, origin='center', displayInline=False)
    canvas = draw.Drawing(WIDTH, HEIGHT, origin='center')
    canvas.append(draw.Rectangle(-20,-HEIGHT,5,25, fill='green'))
    #canvas.append(draw.Rectangle(-20,-20,5,20, fill='purple'))
    canvas.append(draw.Rectangle(-15,-20,5,25, fill='green'))
    canvas.append(
        draw.Line(WIDTH,
                  Y_OFFSET-7,
                  -25,
                  Y_OFFSET-7,
                  stroke='black',
                  stroke_width=0.5,
                  fill='none'))
    '''
    for i, (xx, yy1, yy2) in enumerate(zip(labels, samples[0], samples[1])):
        canvas.append(draw.Rectangle(-10*i, 0, 10, yy1, fill='green'))
        #canvas.append(draw.Rectangle(10*i, yy1, 10, yy2, fill='purple'))
    '''

    canvas.save_svg('../examples')
    #return canvas.asSvg()


# Preview design in the browser
def browser_preview(badge):
    _, badge_path = tempfile.mkstemp(suffix='.svg')
    with open(badge_path, 'w') as f:
        f.write(badge)

    webbrowser.open_new_tab('file://' + badge_path)


x = ['A', 'B', 'C']
y1 = [35, 27, 15]
y2 = [18, 22, 13]
sb1 = stacked_bar(x, (y1, y2))

values = [-10, -10, 32, 16, -3, 30, 25, 20, -15, 10, 5, 7]
t = hist_trend(values, "#d944ea", 1)
#t = trend(values, "#007ec6", 1)

#browser_preview(sb1)

'''
values = [-10, -10, 32, 16, -3, 30, 25, 20, -15, 10, 5, 7]
t = hist_trend(values, "#d944ea", 1)
#values = [1311, 2100, 3333, 598, 800, 1111, 200]
#t = trend(values, "#007ec6", 1)
#t = '<img src=\"' + trend(values, "#d944ea", 1) + '\" alt=\"Test Image\" />'
#t = '<img src=\"' + hist_trend(values, "#d944ea",
#                               1) + '\" alt=\"Test Image\" />'
#f = open('/home/nick/Desktop/badges/trend.svg', 'w')
f = open('/home/nick/Desktop/badges/hist_trend.txt', 'w')
f.write(t)
f.close()
'''
