import base64
import matplotlib.pyplot as plt
from io import BytesIO
import metrics_extract as me


def issue_graph(opened, closed, figsize=(4, 0.25), **kwargs):
    #plt.rc('axes', labelsize=8)
    plt.rc('xtick', labelsize=5)
    fig, ax = plt.subplots(figsize=figsize, **kwargs)
    #x = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    x = ['1/22', '2/22', '3/22', '4/22', '5/22', '6/22', '7/22', '8/22', '9/22', '10/22', '11/22', '12/22']
    #x = [i for i in range(1,13)]
    ax.bar(x, opened, align='edge', width=1, color='green', edgecolor='black')
    ax.bar(x, closed, align='edge', width=1, color='purple', edgecolor='black')
    plt.axhline(y=0.0, color='black', linestyle='-', linewidth=1)

    # Turn off spine/tick visibility
    for _, v in ax.spines.items():
        v.set_visible(False)
    #ax.set_xticks([])
    ax.set_yticks([])

    #plt.show()
    # Base64 encoding
    img = BytesIO()
    plt.savefig(img, transparent=True, bbox_inches='tight')
    img.seek(0)
    plt.close()

    return base64.b64encode(img.read()).decode("UTF-8")

def spark_bar(data, figsize=(4, 0.25), **kwargs):
    fig, ax = plt.subplots(1, 1, figsize=figsize, **kwargs)
    cmap = colormap(data.values())
    ax.bar(data.keys(), data.values(), color=cmap, align='edge', width=1, edgecolor='black')
    plt.axhline(y=0.0, color='black', linestyle='-', linewidth=1)

    # Turn off spine/tick visibility
    for _, v in ax.spines.items():
        v.set_visible(False)
    ax.set_xticks([])
    ax.set_yticks([])


    # Base64 encoding
    img = BytesIO()
    plt.savefig(img, transparent=True, bbox_inches='tight')
    img.seek(0)
    plt.close()

    return base64.b64encode(img.read()).decode("UTF-8")

def spark_bar_test(testX, testY, figsize=(4, 0.25), **kwargs):
    fig, ax = plt.subplots(1, 1, figsize=figsize, **kwargs)
    #cmap = colormap(data.values())
    #ax.bar(data.keys(), data.values(), color=cmap, align='edge', width=1, edgecolor='black')
    cmap = colormap(testY)
    ax.bar(testX, testY, color=cmap, align='edge', width=1, edgecolor='black')
    plt.axhline(y=0.0, color='black', linestyle='-', linewidth=1)

    # Turn off spine/tick visibility
    for _, v in ax.spines.items():
        v.set_visible(False)
    ax.set_xticks([])
    ax.set_yticks([])


    # Base64 encoding
    img = BytesIO()
    plt.savefig(img, transparent=True, bbox_inches='tight')
    img.seek(0)
    plt.close()

    return base64.b64encode(img.read()).decode("UTF-8")


def colormap(data):
    cmap = []
    for d in data:
        if d >= 0:
            cmap.append('green')
        else:
            cmap.append('red')
    return cmap

opened, closed = me.issues('nshan651', 'excite-cli')
print(opened)
issue_graph(opened, closed)
