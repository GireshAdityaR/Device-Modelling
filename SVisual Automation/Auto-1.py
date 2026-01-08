import svisual as sv
x1=-0.5  #X axis minimum value
x2= 4.3858#X axis maximum value
y1=-0.1  #Y axis minimum value
y2=23.04  #Y axis maximum value
n1='7'   # node number for positive voltages
n2='7'   # node number for negative voltages   # fix the resolution of the gif
min_val=0  # starting voltage
max_val=100   # Final voltage
step=1      # step value between voltages
min_conc='None'    # minimum value of the contour legend
max_conc='None'     # maximum value of the contour legend
Field='eDensity'
path='/home/vlsi/TCAD/STDB/dmlmini/hemt_off_ehTemp'
values=[]  #Change the values within square bracknets according to the given voltage, fix other parameters as usual

def Find_min_max(plot,field):
  values=[]
  for i in plot:
    values+=sv.get_field_prop(plot=i,property='range',field=field)
  values.sort()
  return [values[0],values[-1]]
def File_Names(n1,n2,min_val,max_val,step,path,continuous=False,Discrete=False,value=[]):
  zero=''
  count=1
  sign='pos'
  if (len(value)!=0):
    names=[]
    for i in value:
      if i==0:
        sv.load_file(path+'n'+n1+'_Zero_C_des.tdr')
        sv.create_plot(name='n0000',dataset='n'+n1+'_Zero_C_des')
        sv.set_plot_prop(plot='n0000',title='VDS=0V',not_keep_aspect_ratio=True)
        sv.windows_style(style='max')
        names.insert(0,'n0000')
      else:
        if((i<10)&(i>-10)):
          zero='000'
        elif((i<100)&(i>=10)):
          zero='00'
        elif((i<1000)&(i>=100)):
          zero='0'
        elif((i<=-10)&(i>-100)):
          zero='00'
        elif((i<=-100)&(i>-1000)):
          zero='0'
        elif((i==1000) or (i==-1000)):
          zero=''
        if(i>0):
          sign='pos'
          n=n1
          tit_val=i
        else:
          sign='Neg'
          n=n2
          tit_val=i
          i*=-1   
        zero1='0'*(4-len(str(count)))      
        name='n'+zero1+str(count)
        sv.load_file(path+'n'+n+'_ss_'+sign+'_'+zero+str(min_val)+'_C_des.tdr')
        sv.create_plot(name=name,dataset='n'+n+'_ss_'+sign+'_'+zero+str(min_val)+'_C_des')
        names.append(name)
        sv.set_plot_prop(plot=name,title='VDS='+str(i/10)+'V',not_keep_aspect_ratio=True)
        sv.windows_style(style='max')
        count+=1
  else:
    names=[]
    while(min_val<=max_val):
      if(min_val==0):
        sv.load_file(path+'n'+n1+'_Zero_C_des.tdr')
        sv.create_plot(name='n0000',dataset='n'+n1+'_Zero_C_des')
        sv.set_plot_prop(plot='n0000',title='VDS=0V',not_keep_aspect_ratio=True)
        sv.windows_style(style='max')
        names.insert(0,'n0000')
      else:
        if((min_val<10)&(min_val>-10)):
          zero='000'
        elif((min_val<100)&(min_val>=10)):
          zero='00'
        elif((min_val<100)&(min_val>=100)):
          zero='0'
        elif((min_val<=-10)&(min_val>-100)):
          zero='00'
        elif((min_val<=-100)&(min_val>-100)):
          zero='0'
        elif((min_val==100) or (min_val==-100)):
          zero=''
        if(min_val>=0):
          sign='pos'
          n=n1
          tit_val=min_val
        else:
          sign='Neg'
          n=n2
          tit_val=min_val
          min_val*=-1   
        zero1='0'*(4-len(str(count)))      
        name='n'+zero1+str(count)
        sv.load_file(path+'n'+n+'_ss_'+sign+'_'+zero+str(min_val)+'_C_des.tdr')
        sv.create_plot(name=name,dataset='n'+n+'_ss_'+sign+'_'+zero+str(min_val)+'_C_des')
        names.append(name)
        sv.set_plot_prop(plot=name,title='VGS='+str(tit_val/10)+'V',not_keep_aspect_ratio=True)
        count+=1
      min_val+=step
  return names
def Fix_properties(Field,names,x1,x2,y1,y2,min=None,max=None,contour=True):
  sv.start_movie()
  if (min==None)&(max==None):
    range=Find_min_max(names,Field)
    min=range[0]
    max=range[-1]
  for i in names:
    sv.set_field_prop(plot=i,max=max, min=min,max_fixed=True,min_fixed=True,field=Field,show_bands=True,show=contour,contour_labels_off=True)
    sv.set_axis_prop(plot=i,axis='x',range=[str(x1),str(x2)])
    sv.set_axis_prop(plot=i,axis='y',range=[str(y1),str(y2)])
  for i in names:
    sv.select_plots([i])
    sv.windows_style(style='max')
    sv.add_frame(i)
    sv.set_field_prop(plot=i,field=Field,show_bands=True,hide=True,contour_labels_off=True)
names=File_Names(n1,n2,min_val,max_val,step,path,Discrete=True,value=values)
Fix_properties(Field,names,x1,x2,y1,y2)
