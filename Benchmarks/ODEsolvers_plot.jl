function evaluate_ODEsolvers(saveat, data)
	# A function to evaluate the ODE solvers performance in terms of simluation time. 
	# The tested solvers are the implicit stiff solvers, FBDF, QBDF and QNDF. 
	# Four different options are tested. All of them include a prototype Jacobian. 
	# The options are: No Jacobian, with Jacobian, no preconditioning and with preconditioning
	# The preconditioner is performed using the incompleteLU. 
	
	

		
	names1 = ["FBDF","QNDF","QBDF"]
	names2 = ["FBDF_jac","QNDF_jac","QBDF_jac"]
	names3 = ["FBDF_prec","QNDF_prec","QBDF_prec"]
	names4 = ["FBDF_precJac","QNDF_precJac","QBDF_precJac"]
	
	nCell = unique(data.nCellu)
	polyDegPore = unique(data.polyDegPoreu)
	polyDeg = unique(data.polyDegu)
	solvers = [1,2,3]

	# Colors for the plots 
	color1 = palette([:green,:red],4)
	color2 = palette([:purple, :grey],4)
	color3 = palette([:blue,:yellow],4)
	markers = [:hex, :d, :star]
	
	
	#Initialize plots
	p1 = plot()
	p2 = plot()
	p3 = plot()


	# Loop through solver setups and other parameters
    for i =1:size(solvers)[1] # i=1
		
		for h=1:length(polyDegPore)
			for j=1:size(polyDeg)[1]
				for k=1:4	# k=1

					# Insert in plots 
					idx = 1 + (i-1)*length(nCell):length(nCell) + (i-1)*length(nCell)

					# If not evaluating that specific solver option, skip the iteration 
					if data[idx, Symbol("maxE_m$k")][1] == 0
						continue
					else

						# dof error
						plot!(p1, data[idx,:DOF], data[idx, Symbol("maxE_m$k")], xaxis=:log, yaxis=:log, marker=markers[i], linestyle=:dot, label=eval(Symbol("names$k"))[i],color = eval(Symbol("color$i"))[k], markersize = 5)

						# dof runtime
						plot!(p2, data[idx,:DOF], data[idx, Symbol("runtime_m$k")], marker=markers[i], linestyle=:dot, label=eval(Symbol("names$k"))[i],color = eval(Symbol("color$i"))[k], markersize = 5)

						# runtime error plot
						plot!(p3, data[idx,Symbol("runtime_m$k")], data[idx, Symbol("maxE_m$k")], xaxis=:log, yaxis=:log, marker=markers[i], linestyle=:dot, label=eval(Symbol("names$k"))[i],color = eval(Symbol("color$i"))[k], markersize = 5)
					end
				end
			end
		end
	end
	
	# Insert in plots 
	# if hasproperty(data, :maxE_ida)
	# 	colorIDA = palette([:cyan,:blue],4)
	# 	for i = 1:size(polyDeg)[1]
	# 		idx = 1 + (i-1)*length(nCell):length(nCell) + (i-1)*length(nCell)

	# 		# dof error
	# 		plot!(p1, data[idx, :DOF], data[idx, :maxE_ida], xaxis=:log, yaxis=:log, marker=:utriangle, linestyle=:dot, label="IDA",color = colorIDA[1], markersize = 5)
	# 		plot!(p1, data[idx, :DOF], data[idx, :maxE_ida_jac], xaxis=:log, yaxis=:log, marker=:utriangle, linestyle=:dot, label="IDA_jac",color = colorIDA[2], markersize = 5)

	# 		# dof runtime
	# 		plot!(p2, data[idx, :DOF], data[idx, :runtime_ida], marker=:utriangle, linestyle=:dot, label="IDA",color = colorIDA[1], markersize = 5)
	# 		plot!(p2, data[idx, :DOF], data[idx, :runtime_ida_jac], marker=:utriangle, linestyle=:dot, label="IDA_jac",color = colorIDA[2], markersize = 5)

	# 		# runtime error plot
	# 		plot!(p3, data[idx, :runtime_ida], data[idx, :maxE_ida], xaxis=:log, yaxis=:log, marker=:utriangle, linestyle=:dot, label="IDA",color = colorIDA[1], markersize = 5)
	# 		plot!(p3, data[idx, :runtime_ida_jac], data[idx, :maxE_ida_jac], xaxis=:log, yaxis=:log, marker=:utriangle, linestyle=:dot, label="IDA_jac",color = colorIDA[2], markersize = 5)

	# 	end
	# end
	
	#Axis options for the plot
	plot!(p1,xaxis="Degrees of freedom", yaxis="Max abs error (mol/m\$^3\$)", grid=true, legend = :best)
	plot!(p2,xaxis="Degrees of freedom", yaxis="Simulation time (s)", grid=true, legend = :best)
	plot!(p3,xaxis="Simulation time (s)", yaxis="Abs max error (mol/m\$^3\$)", grid=true, legend = :best)


	display(p1)
	display(p2)
	display(p3)

	savefig(p1,joinpath(saveat,"Convergence.svg"))
	savefig(p2,joinpath(saveat,"Runtime.svg"))
	savefig(p3,joinpath(saveat,"RuntimeError.svg"))


	
	
	nothing 
end	

using CSV, DataFrames, Plots


# LRM, Linear
path = joinpath(@__DIR__,"Linear/batch/LRM/ODETests")
data = CSV.read(joinpath(path,"ODESolverResults.csv"), DataFrame)
evaluate_ODEsolvers(path, data)

# LRMP, Linear
path = joinpath(@__DIR__,"Linear/batch/LRMP/ODETests")
data = CSV.read(joinpath(path,"ODESolverResults.csv"), DataFrame)
evaluate_ODEsolvers(path, data)

# GRM, Linear
path = joinpath(@__DIR__,"Linear/batch/GRM/ODETests")
data = CSV.read(joinpath(path,"ODESolverResults.csv"), DataFrame)
evaluate_ODEsolvers(path, data)


# LRM, Langmuir
path = joinpath(@__DIR__,"Langmuir/batch/LRM/ODETests")
data = CSV.read(joinpath(path,"ODESolverResults.csv"), DataFrame)
evaluate_ODEsolvers(path, data)

# LRMP, Langmuir
path = joinpath(@__DIR__,"Langmuir/batch/LRMP/ODETests")
data = CSV.read(joinpath(path,"ODESolverResults.csv"), DataFrame)
evaluate_ODEsolvers(path, data)

# GRM, Langmuir
path = joinpath(@__DIR__,"Langmuir/batch/GRM/ODETests")
data = CSV.read(joinpath(path,"ODESolverResults.csv"), DataFrame)
evaluate_ODEsolvers(path, data)



# LRMP, SMA
path = joinpath(@__DIR__,"SMA/batch/LRMP/ODETests")
data = CSV.read(joinpath(path,"ODESolverResults.csv"), DataFrame)
evaluate_ODEsolvers(path, data)

# GRM, SMA
path = joinpath(@__DIR__,"SMA/batch/GRM/ODETests")
data = CSV.read(joinpath(path,"ODESolverResults.csv"), DataFrame)
evaluate_ODEsolvers(path, data)


