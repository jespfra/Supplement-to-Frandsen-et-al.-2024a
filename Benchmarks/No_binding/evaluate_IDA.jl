function evaluate_IDA(c_analytical, nComp, nCell, polyDeg, polyDegPore::Union{Int64,Vector{Int64}}, transport_model, saveat, alg)
	# A function to evaluate the IDA solver, but with and without Jacobian
	# Problems are solved with and without Jacobian 
	
	# Check for correct typed transport model 
	if transport_model != "LRM" && transport_model != "LRMP" && transport_model != "GRM"
		throw("Incorrect Transport model")
	end

	

	#Preload the data vectors
	maxE_m1 =[] # with Jacobian
	
	runtime_m1 = []

	DOF = []
	nCellu = []
	polyDegu = []
	polyDegPoreu = []
	


	# Loop through solver setups and other parameters
	for h=1:length(polyDegPore)
		for j=1:size(polyDeg)[1]
			for k=1:size(nCell)[1]
				println("polyDegPore = $(polyDegPore[h])")
				println("polyDeg = $(polyDeg[j])")
				println("nCell = $(nCell[k])")
				
				# Solve without analytical Jacobian
				if transport_model == "GRM"
					inlets, outlets, columns, switches, solverOptions = model_setup(nCell[k],polyDeg[j], polyDegPore[h], 0, true)
					rtime = @elapsed solve_model_dae(columns = columns,switches = switches,solverOptions = solverOptions, outlets = outlets, alg = alg)
				else 
					inlets, outlets, columns, switches, solverOptions = model_setup(nCell[k],polyDeg[j], 0, true)
					rtime = @elapsed solve_model_dae(columns = columns,switches = switches,solverOptions = solverOptions, outlets = outlets, alg = alg)
				end
				err = 0
				for n = 0:size(outlets[1].solution_outlet)[2]-1
					err = maximum([err, maximum(abs.(outlets[1].solution_outlet[:,n+1]-c_analytical[:,"C$n"]))])
				end
				
				# Store data
				append!(maxE_m1, err)
				append!(runtime_m1, rtime)
				
				
				# Store additional data 
				append!(nCellu,nCell[k])
				append!(polyDegu,polyDeg[j])
				append!(polyDegPoreu,polyDegPore[h])

				#Depending on the model, the DOF is different
				if transport_model == "LRM"
					append!(DOF,2*nCell[k]*nComp*(polyDeg[j]+1))
				elseif transport_model == "LRMP"
					append!(DOF,3*nCell[k]*nComp*(polyDeg[j]+1))
				elseif transport_model == "GRM"
					append!(DOF,nComp*(polyDeg[j]+1)*nCell[k] + nComp*(polyDeg[j]+1)*nCell[k]*(polyDegPore[h]+1)*2) 
				end
			end
			
		end
	end
	
	
	df = DataFrame(runtime_m1=runtime_m1,
	maxE_m1=maxE_m1,
	DOF=DOF,nCellu=nCellu,polyDegu=polyDegu, polyDegPoreu=polyDegPoreu)
	CSV.write(joinpath(saveat,"CADETJuliaConvergence.csv"),df)
	
	
	nothing 
end	
