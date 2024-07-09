

import pandas as pd
	
	
def runCadetDG(transportModel, c_analytical, polyDeg, nCells, runKin,polyDegPore=0,nCellsPar=1):
    
    DOF = []
    nCellu = []
    polyDegu = []
    nCellsParu = []
    polyDegPoreu = []
    maxE_e = []
    maxE_i = []
    maxE_e_ode = []
    maxE_i_ode = []
    runtime_e = []
    runtime_i = []
    runtime_e_ode = []
    runtime_i_ode = []

    
    if transportModel != "GRM":
        iterPoly = polyDeg
    else:
        iterPoly = polyDegPore
    
    # Run simulations
    for i in range(0, len(iterPoly)):
        for l in range(0, len(nCells)):
            print(f'Polynomial order {iterPoly[i]}')
            print(f'Column discretization {nCells[l]}')
    
            if transportModel != "GRM":
                t, c, runtime = run_simulation(transportModel, nCells[l], polyDeg[i], True, False)
            else:
                t, c, runtime = run_simulation_GRM(transportModel, nCells[l], polyDeg, polyDegPore[i], nCellsPar, True, False)
    
            runtime_e.append(runtime)
            err = 0
            for k in range(c.shape[1]):  # Number of components
                idxx = f'C{k}'
                err = max([err, abs(c[:, k] - c_analytical[idxx][:]).max()])
            maxE_e.append(err)
    
            if transportModel != "GRM":
                t, c, runtime = run_simulation(transportModel, nCells[l], polyDeg[i], False, False)
            else:
                t, c, runtime = run_simulation_GRM(transportModel, nCells[l], polyDeg, polyDegPore[i], nCellsPar, False, False)
    
            runtime_i.append(runtime)
            err = 0
            for k in range(c.shape[1]):  # Number of components
                idxx = f'C{k}'
                err = max([err, abs(c[:, k] - c_analytical[idxx][:]).max()])
            maxE_i.append(err)
            
            
            if runKin==True:
                if transportModel != "GRM":
                    t, c, runtime = run_simulation(transportModel, nCells[l], polyDeg[i], True, 1)
                else:
                    t, c, runtime = run_simulation_GRM(transportModel, nCells[l], polyDeg, polyDegPore[i],nCellsPar, 1, 1)
                    
                runtime_e_ode.append(runtime)
                err = 0
                for k in range(c.shape[1]): #Number of components            
                    idxx = f'C{k}'
                    err = max([err,abs(c[:, k] - c_analytical[idxx][:]).max()])
                maxE_e_ode.append(err)
                
                
                if transportModel != "GRM":
                    t, c, runtime = run_simulation(transportModel, nCells[l], polyDeg[i], False, 1)
                else:
                    t, c, runtime = run_simulation_GRM(transportModel, nCells[l], polyDeg, polyDegPore[i],nCellsPar, 0, 1)
                runtime_i_ode.append(runtime)
                err = 0
                for k in range(c.shape[1]): #Number of components            
                    idxx = f'C{k}'
                    err = max([err,abs(c[:, k] - c_analytical[idxx][:]).max()])
                maxE_i_ode.append(err)
            
            
            
            nCellu.append(nCells[l])
            polyDegu.append(iterPoly[i])
            polyDegPoreu.append(iterPoly[i])
            nCellsParu.append(nCellsPar)
            
            if transportModel == "LRM":
                DOF.append(c.shape[1] * nCells[l] * (polyDeg[i] + 1) * 2)  # 2 phases
            elif transportModel == "LRMP":
                DOF.append(c.shape[1] * nCells[l] * (polyDeg[i] + 1) * 3)  # 3 phases
            elif transportModel == "GRM":
                DOF.append(c.shape[1] * nCells[l] * (polyDeg + 1)  + c.shape[1]*2*nCells[l] * (polyDeg + 1)*(polyDegPore[i]+1) * nCellsPar)

            
            # Save results everytime a simulation as been carried out 
            if runKin == True and transportModel != "GRM":	   
                convergenceDataDG = pd.DataFrame({'DOF': DOF, 'nCellu': nCellu,'polyDegu': polyDegu,'runtime_e': runtime_e,'maxE_e': maxE_e,'runtime_i': runtime_i,'maxE_i': maxE_i,
                                                  'runtime_e_ode': runtime_e_ode,'maxE_e_ode': maxE_e_ode,'runtime_i_ode': runtime_i_ode,'maxE_i_ode': maxE_i_ode,})
            elif runKin == False and transportModel != "GRM":
                convergenceDataDG = pd.DataFrame({'DOF': DOF, 'nCellu': nCellu,'polyDegu': polyDegu,'runtime_e': runtime_e,'maxE_e': maxE_e,'runtime_i': runtime_i,'maxE_i': maxE_i,})
            elif runKin == True and transportModel == "GRM":
                convergenceDataDG = pd.DataFrame({'DOF': DOF, 'nCellu': nCellu,'polyDegPoreu': polyDegPoreu, 'polyDegPoreu' : polyDegPoreu, 'nCellsParu' : nCellsParu,'runtime_e': runtime_e,'maxE_e': maxE_e,'runtime_i': runtime_i,'maxE_i': maxE_i,
                                                  'runtime_e_ode': runtime_e_ode,'maxE_e_ode': maxE_e_ode,'runtime_i_ode': runtime_i_ode,'maxE_i_ode': maxE_i_ode,})
            elif runKin == False and transportModel == "GRM":
                convergenceDataDG = pd.DataFrame({'DOF': DOF, 'nCellu': nCellu,'polyDegPoreu': polyDegPoreu, 'polyDegPoreu' : polyDegPoreu, 'nCellsParu' : nCellsParu,'runtime_e': runtime_e,'maxE_e': maxE_e,'runtime_i': runtime_i,'maxE_i': maxE_i,})
            #Save data in a CSV file
            # save results for in GSM results in case study folder
            convergenceDataDG.to_csv('CADETDGConvergence.csv')
                   
	
def runCadetGSM(transportModel, c_analytical, polyDeg, nCells, polyDegPore,nCellsPar):
    # For the DGSEM GSM comparison, we set the nCells in the bulk to 8. 
    # The benchmarks are only for collocation DGSEM and GSM 
    # First, varying the polynomial degree in the pore phase while fixing the particle phase elements to 1 for GSM (default) and DGSEM  
    # Then, the elements and polynomial degree in the particle phase is increased
    

    DOF = []
    nCellu = []
    polyDegu = []
    nCellsParu = []
    polyDegPoreu = []
    maxE_e = []
    maxE_i = []
    runtime_e = []
    runtime_i = []

    
    
    
    iterPoly = polyDegPore
    
    # Run simulations
    for p in range(len(nCellsPar)):
        for i in range(0, len(iterPoly)):
            print(f'Polynomial order {iterPoly[i]}')
            print(f'Par elements {nCellsPar[p]}')
            
            # Arguments in run_simulation_GRM 
            # transportModel, ncol, polydeg,polyDegPore, nCellsPar, is_exact,is_ode, analJac = True, par_gsm=True
            
            # Run simulations where GSM is used for a single element 
            err = 0
            runtime = 0
            if p == 0:
                t, c, runtime = run_simulation_GRM(transportModel, nCells, polyDeg, polyDegPore[i], nCellsPar[p], 0, 0, True, True)
                
                for k in range(c.shape[1]):  # Number of components
                    idxx = f'C{k}'
                    err = max([err, abs(c[:, k] - c_analytical[idxx][:]).max()])
            runtime_e.append(runtime)
            maxE_e.append(err)
    
 

            # Run at par_gsm = False for varying particle polynomial degree and elements
            err = 0
            runtime = 0
            # For multiple particle cell, we do not want to run more than 10 polynomials degrees in the particle phase
            if nCellsPar[p]>1 and polyDegPore[i]>10:
                print("Simulation skipped") 
            else:
                # For par elements = 1
                t, c, runtime = run_simulation_GRM(transportModel, nCells, polyDeg, polyDegPore[i], nCellsPar[p], 0, 0, True, False)
                for k in range(c.shape[1]):  # Number of components
                    idxx = f'C{k}'
                    err = max([err, abs(c[:, k] - c_analytical[idxx][:]).max()])
    
            runtime_i.append(runtime)
            maxE_i.append(err)
    
           
            
            nCellu.append(nCells)
            polyDegu.append(iterPoly[i])
            polyDegPoreu.append(iterPoly[i])
            nCellsParu.append(nCellsPar[p])
            
           
            
            DOF.append(c.shape[1] * nCells * (polyDeg + 1)  + c.shape[1]*2*nCells * (polyDeg + 1)*(polyDegPore[i]+1) * nCellsPar[p])

            
            # Save results everytime a simulation as been carried out 
            convergenceDataDG = pd.DataFrame({'DOF': DOF, 'nCellu': nCellu,'polyDegu': polyDegu, 'polyDegPoreu' : polyDegPoreu, 'nCellsParu' : nCellsParu,'runtime_e': runtime_e,'maxE_e': maxE_e,'runtime_i': runtime_i,'maxE_i': maxE_i})
            #Save data in a CSV file
            # save results of GSM-DGSEM comparisons in GSM folder
            convergenceDataDG.to_csv('GSM/CADETDGConvergence.csv')
            
	
# Run simulation for LRM and LRMP
def run_simulation(transportModel, ncol, polydeg, is_exact, is_ode, analJac = True):
    rtimes = [0,0,0]
    for i in range(3): # run 3 simulations 
        t, c, rtime = model(ncol, polydeg, is_exact,is_ode, analJac)
        rtimes[i] = rtime
        time.sleep(2)
        if len(t)<5: # If simulation crashed, store the rtime as 666
            rtimes[i] = 666
        
    return t,c,min(rtimes)
    
    
# Run simulation GRM
def run_simulation_GRM(transportModel, ncol, polydeg,polyDegPore, nCellsPar, is_exact,is_ode, analJac = True, par_gsm=True):
    rtimes = [0,0,0]
    for i in range(3): # run 3 simulations 
        t, c, rtime = model(ncol, polydeg,polyDegPore, nCellsPar, is_exact,is_ode, analJac, par_gsm)
        rtimes[i] = rtime
        time.sleep(2)
        if len(t)<5: # If simulation crashed, store the rtime as 666
            rtimes[i] = 666
        
    return t,c,min(rtimes)
	
