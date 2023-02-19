import os
import numpy as np
import badges
import metrics_extract as me


def main():
    #actions_workflows('nshan651', 'Course-Archive')
    #actions_jobs('nshan651', 'Course-Archive')
    #xtick_labels = ['2022-06-11T18:54:12Z', '2022-06-11T18:51:35Z', '2022-06-11T18:51:35Z', '2022-06-11T18:42:36Z']
    values = {'ID:2480945374' : -10.0, 'ID:2480938429' : -10.0, 'ID:2480938427' : 18.0, 'ID:2480914715' : 16.0}
    testY = [-10.0, -10.0, 32.0, 16.0, -3.0, 30.0, 25.0, 20.0, -15.0, 10.0, 5.0, 7.0]
    testX = np.arange(1, len(testY)+1, 1) 

    #me.actions_runs('nshan651', 'Course-Archive')

    opened, closed = me.issues('nshan651', 'excite-cli')

    badge_path = '/home/nick/git/sparkbadge' 
    # Open an read in html template as a single string
    template_file = open(f'{badge_path}/template.html', 'r')
    template = template_file.read()

    # Inject base64 image into html template
    # figsize=(3,0.5)
    base64_img = f'<div><img src="data:image/png;base64,{badges.spark_bar_test(testX, testY, figsize=(4,0.75))}"/></div>'
    #base64_img = f'<div><img src="data:image/png;base64,{badges.issue_graph(opened, closed, figsize=(4,0.75))}"/></div>'
    template = template.replace('<!-- IMG -->', base64_img)
    template_file.close()
    
    # Write to output
    output_file = open(f'{badge_path}/badge.html', 'w')
    output_file.write(template)
    output_file.close()
    
    # Convert template to svg
    os.system(f'wkhtmltoimage {badge_path}/badge.html {badge_path}/badge_tmp.svg')
    
    # Modify svg to remove white background 
    os.system('''awk '/<g fill/{c+=1}{if(c==2 || c==6 || c==7){sub("<g fill=\\"#ffffff\\"","<g fill=\\"none\\"",$0)};print}' ''' +  f'{badge_path}/badge_tmp.svg' + " > " +  f'{badge_path}/badge.svg') 

    # Remove temp svg
    os.system(f'rm {badge_path}/badge_tmp.svg')

if __name__ == "__main__":
    main()
