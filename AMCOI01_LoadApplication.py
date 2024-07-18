# -*- coding: mbcs -*-
# Do not delete the following import lines
from abaqus import *
from abaqusConstants import *
import __main__

import section
import regionToolset
import displayGroupMdbToolset as dgm
import part
import material
import assembly
import step
import interaction
import load
import mesh
import optimization
import job
import sketch
import visualization
import xyPlot
import displayGroupOdbToolset as dgo
import connectorBehavior

muscle_names = ['addbrev_r', 'addlong_r', 'addmagDist_r', 'addmagIsch_r', 'addmagMid_r', 'addmagProx_r', 'bflh140_r', 'gem_r', 'glmax1_r', 'glmax2_r', 'glmax3_r', 'glmed1_r', 'glmed2_r', 'glmed3_r', 'glmin1_r', 'glmin2_r', 'glmin3_r', 'grac_r', 'iliacus_r', 'obtext_r', 'obtint_r', 'pect_r', 'piri_r', 'psoas_r', 'quadfem_r', 'recfem_r', 'sart_r', 'semimem_r', 'semiten_r', 'tfl_r']
xs = [-32.5, -34.5, -34.5, -31.5, -30.5, -38.5, -26.5, -21.5, -36.5, -34.5, -31.5, -13.5, -26.5, -35.5, 3.5, -4.5, -13.5, -5.5, -32.5, -27.5, -18.5, -39.5, -21.5, -33.5, -30.5, -2.5, -8.5, -27.5, -20.5, -19.5]
ys = [-113.5, -271.5, -270.5, -209.5, -148.5, -84.5, -269.5, -1.5, -65.5, -99.5, -129.5, -5.5, 2.5, 4.5, -13.5, -7.5, 0.5000000000002001, -269.5, -69.5, -17.5, -5.5, -64.5, -11.5, -62.5, -34.5, -268.5, -269.5, -268.5, -270.5, -269.5]
zs = [31.5, 21.5, 27.5, 27.5, 29.5, 35.5, 36.5, 43.5, 50.5, 44.5, 41.5, 62.5, 53.5, 40.5, 51.5, 55.5, 56.5, 33.5, 5.5, 42.5, 43.5, 30.5, 43.5, 3.5, 22.5, 23.5, 10.5, 14.5, 11.5, 39.5]

a = mdb.models['TF model'].rootAssembly
n1 = a.instances['PART-1-1'].nodes

for i in range(len(muscle_names)):
    nodes1 = n1.getByBoundingBox(xs[i] - 0.5, ys[i] - 0.5, zs[i] - 0.5, xs[i] + 0.5, ys[i] + 0.5, zs[i] + 0.5)
    region = regionToolset.Region(nodes=nodes1)
    mdb.models['TF model'].ConcentratedForce(name=muscle_names[i], createStepName='Step-1', 
        region=region, cf1=1.0, cf2=2.0, cf3=3.0, distributionType=UNIFORM, 
        field='', localCsys=None)
    # mdb.models['FemurOI'].ConcentratedForce(name='Load-4', createStepName='Step-1', 
    #     region=region, cf1=1.0, cf2=2.0, cf3=3.0, distributionType=UNIFORM, 
    #     field='', localCsys=None)


