import math
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt1
import numpy as np

from flask import Flask, render_template, request, redirect, url_for, send_from_directory,jsonify

#function definition to calculate the resource balancing factor given the resources utilized as input parameters (cpu,ram,network)
def skewness(cpu,ram,network):
     averagePMTotalResources = ((cpu+ram+network)/3.0)  
     skewFactor_one =(cpu/averagePMTotalResources-1) ** 2;     
     skewFactor_two =(ram/averagePMTotalResources-1) ** 2;
     skewFactor_three =(network/averagePMTotalResources-1) ** 2;  
     skewness = math.sqrt((skewFactor_one+skewFactor_two+skewFactor_three));
     return skewness
     
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['ALLOWED_EXTENSIONS'] = set(['jpg', 'jpeg','png','JPG'])


@app.route('/')
@app.route('/index', methods=["GET","POST"])
def index():
    return render_template('index.html')


@app.route('/translate')
def translate():
     
     pmVal1 = request.args.get('textVal', 0, type=str)
     pmVal2 = request.args.get('textVal1', 0, type=str)
     pmVal3 = request.args.get('textVal2', 0, type=str)
     vmVal4 = request.args.get('textVal3', 0, type=str)
     vmVal5 = request.args.get('textVal4', 0, type=str)
     vmVal6 = request.args.get('textVal5', 0, type=str)
    #intializing physical machine resources
     physicalMachineResources_1 = [int(e) if e.isdigit() else e for e in pmVal1.split(',')]
     physicalMachineResources_2 = [int(e) if e.isdigit() else e for e in pmVal2.split(',')]
     physicalMachineResources_3 = [int(e) if e.isdigit() else e for e in pmVal3.split(',')]


     #initializing virtual machine resources
     vmResources_1 = [int(e) if e.isdigit() else e for e in vmVal4.split(',')]
     vmResources_2 = [int(e) if e.isdigit() else e for e in vmVal5.split(',')]
     vmResources_3 = [int(e) if e.isdigit() else e for e in vmVal6.split(',')]


        
     # calculating the initial RBF/Skewness of the physical machines
     initialRBF = [None]*len(physicalMachineResources_1)
     for i in range(0,len(physicalMachineResources_1)):
          initialRBF[i] = skewness(physicalMachineResources_1[i],physicalMachineResources_2[i],physicalMachineResources_3[i]);

     print("Before Allocation")
     print("PM Resource 1")
     print(physicalMachineResources_1)
     print("PM Resource 2")
     print(physicalMachineResources_2)
     print("PM Resource 3")
     print(physicalMachineResources_3)
     print("PM RBF ")
     print(initialRBF);


     #plotting the graph before virtual machine allocation(RBF Graph)
     plt1.ylim((0,3))
     plt1.plot(range(len(physicalMachineResources_1)), initialRBF,label='rbf before allocation')
     plt1.xlabel('Physical Machines')
     plt1.ylabel('Resource Balancing Factor')

     plt1.savefig('uploads/before_alloc.png')


     #Bar graph of utilized resources in each physical machines
     ind = np.arange(len(physicalMachineResources_1))  # the x locations for the groups
     width = 0.25       # the width of the bars
     plt.ylim([0,200])
     fig, ax = plt.subplots()
     rects1 = ax.bar(ind, physicalMachineResources_1 , width, color='r',label="CPU")
     rects2 = ax.bar(ind+width, physicalMachineResources_2 , width, color='y',label="RAM")
     rects3 = ax.bar(ind+(width*2), physicalMachineResources_3 , width, color='b',label="Network")

     ax.set_ylabel('PM Resources')
     ax.set_title('Resource (CPU,RAM,Network) % before VM allocation')
     ax.set_xticks(ind+width,range(len(physicalMachineResources_1)))

     lgd = plt.legend(loc='best')
     plt.savefig('uploads/image_output1.png', dpi=300, format='png', bbox_extra_artists=(lgd,), bbox_inches='tight')


     plt.savefig('uploads/per_beforeallocation.png')
     plt.close()


     # choosing the best fit PM to allocate the VM
     allocRBF  = [None]*len(physicalMachineResources_1)

     for i in range (0,len(vmResources_1)):
          for j in range(0,len(physicalMachineResources_1)):
               if((physicalMachineResources_1[j]+vmResources_1[i] > 100) or (physicalMachineResources_2[j]+vmResources_2[i] > 100) or (physicalMachineResources_3[j]+vmResources_3[i] > 100) ):
                    allocRBF[j] = 1000;
                    continue;
               else:
                    arg1 = physicalMachineResources_1[j]+vmResources_1[i];
                    arg2 = physicalMachineResources_2[j]+vmResources_2[i];
                    arg3 = physicalMachineResources_3[j]+vmResources_3[i];
                    
                    allocRBF[j] =  skewness(arg1,arg2,arg3);

          #RBF difference 
          diffRBF  = [None]*len(physicalMachineResources_1)
          maxVal = -100
          maxIndex = -100
          for j in range(0,len(physicalMachineResources_1)):
               diffRBF[j] = initialRBF[j] - allocRBF[j];
               if(diffRBF[j] > maxVal):
                    maxVal = diffRBF[j]
                    maxIndex = j
               
          #allocate vm resource to best fit
          if(maxIndex >= 0):
               physicalMachineResources_1[maxIndex] = physicalMachineResources_1[maxIndex] + vmResources_1[i];
               physicalMachineResources_2[maxIndex] = physicalMachineResources_2[maxIndex] + vmResources_2[i];
               physicalMachineResources_3[maxIndex] = physicalMachineResources_3[maxIndex] + vmResources_3[i];
          
          for k in range(0,len(physicalMachineResources_1)):
               initialRBF[k] = skewness(physicalMachineResources_1[k],physicalMachineResources_2[k],physicalMachineResources_3[k]);

     print("After Allocation")
     print("PM Resource 1")
     print(physicalMachineResources_1)
     print("PM Resource 2")
     print(physicalMachineResources_2)
     print("PM Resource 3")
     print(physicalMachineResources_3)
     print("PM RBF ")
     print(initialRBF);

     #plotting the graph after virtual machine allocation(RBF Graph)
     plt1.ylim((0,3))
     plt1.plot(range(len(physicalMachineResources_1)), initialRBF,label='rbf after allocation')
     plt1.xlabel('Physical Machines')
     plt1.ylabel('Resource Balancing Factor')

     plt1.savefig('uploads/after_alloc.png')

     lgd = plt1.legend(loc='best')
     plt1.savefig('uploads/image_output.png', dpi=300, format='png', bbox_extra_artists=(lgd,), bbox_inches='tight')
     plt1.close()

     #Bar graph of utilized resources in each physical machines (after allocation)
     ind = np.arange(len(physicalMachineResources_1))  # the x locations for the groups
     width = 0.25       # the width of the bars
     low = 0
     high = 200
     plt.ylim([math.ceil(low-0.5*(high-low)), math.ceil(high+0.5*(high-low))])
     fig, ax = plt.subplots()
     rects1 = ax.bar(ind, physicalMachineResources_1 , width, color='r',label="CPU")
     rects2 = ax.bar(ind+width, physicalMachineResources_2 , width, color='y',label="RAM")
     rects3 = ax.bar(ind+(width*2), physicalMachineResources_3 , width, color='b',label="Network")

     ax.set_ylabel('PM Resources')
     ax.set_title('Resource (CPU,RAM,Network) % after VM allocation')
     ax.set_xticks(ind+width,range(len(physicalMachineResources_1)))


     lgd = plt.legend(loc='best')
     plt.savefig('uploads/image_output2.png', dpi=300, format='png', bbox_extra_artists=(lgd,), bbox_inches='tight')

     plt.savefig('uploads/per_afterallocation.png')
     plt.close()
     return jsonify(result = 'Graph generated')

@app.route('/upload', methods=['POST'])
def upload():
     if 'RBF' in request.form['submit']:
          return redirect(url_for('uploaded_file',filename="image_output.png"))
     elif 'Before' in request.form['submit']:
          return redirect(url_for('uploaded_file',filename="image_output1.png"))
     elif 'After' in request.form['submit']:
          return redirect(url_for('uploaded_file',filename="image_output2.png"))

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)
if __name__ == "__main__":
    app.run(debug=True)
