

# Add the include file custom to load packages and scripts. 
# the file is located on the main from which the file takes care of the rest. 
include(joinpath(@__DIR__,"..\\..\\include.jl"))



# Define the dictionary representing the model structure
nComp = 1
model = OrderedDict(
    "root" => OrderedDict(
        "input" => OrderedDict(
            "model" => OrderedDict()
        )
    )
)


# Set elements sequentially for unit_000
model["root"]["input"]["model"]["unit_000"] = OrderedDict()
model["root"]["input"]["model"]["unit_000"]["unit_type"] = "INLET"
model["root"]["input"]["model"]["unit_000"]["ncomp"] = nComp
model["root"]["input"]["model"]["unit_000"]["inlet_type"] = "PIECEWISE_CUBIC_POLY"

model["root"]["input"]["model"]["unit_000"]["sec_000"] = OrderedDict()
model["root"]["input"]["model"]["unit_000"]["sec_000"]["const_coeff"] = [1]
model["root"]["input"]["model"]["unit_000"]["sec_001"] = OrderedDict()
model["root"]["input"]["model"]["unit_000"]["sec_001"]["const_coeff"] = [0]


# Set elements sequentially for unit_001
model["root"]["input"]["model"]["unit_001"] = OrderedDict()
model["root"]["input"]["model"]["unit_001"]["unit_type"] = "LUMPED_RATE_MODEL_WITHOUT_PORES"
model["root"]["input"]["model"]["unit_001"]["ncomp"] = nComp
model["root"]["input"]["model"]["unit_001"]["col_porosity"] = 0.6
model["root"]["input"]["model"]["unit_001"]["col_dispersion"] = 1e-4
model["root"]["input"]["model"]["unit_001"]["col_length"] = 1
model["root"]["input"]["model"]["unit_001"]["velocity"] = 2/60
model["root"]["input"]["model"]["unit_001"]["adsorption_model"] = "LINEAR"

model["root"]["input"]["model"]["unit_001"]["adsorption"] = OrderedDict()
model["root"]["input"]["model"]["unit_001"]["adsorption"]["is_kinetic"] = true
model["root"]["input"]["model"]["unit_001"]["adsorption"]["LIN_KA"] = [0.0]
model["root"]["input"]["model"]["unit_001"]["adsorption"]["LIN_KD"] = [0.0]

model["root"]["input"]["model"]["unit_001"]["init_c"] = [0]
model["root"]["input"]["model"]["unit_001"]["init_q"] = [0]

model["root"]["input"]["model"]["unit_001"]["discretization"] = OrderedDict()
model["root"]["input"]["model"]["unit_001"]["discretization"]["polyDeg"] = 4
model["root"]["input"]["model"]["unit_001"]["discretization"]["ncol"] = 16
model["root"]["input"]["model"]["unit_001"]["discretization"]["exact_integration"] = 1
model["root"]["input"]["model"]["unit_001"]["discretization"]["use_analytic_jacobian"] = true
model["root"]["input"]["model"]["unit_001"]["discretization"]["nbound"] = ones(Bool, nComp)

# Set elements for unit_002
model["root"]["input"]["model"]["unit_002"] = OrderedDict()
model["root"]["input"]["model"]["unit_002"]["unit_type"] = "OUTLET"
model["root"]["input"]["model"]["unit_002"]["ncomp"] = nComp


# Set elements for solver
model["root"]["input"]["solver"] = OrderedDict("sections" => OrderedDict())
model["root"]["input"]["solver"]["sections"]["nsec"] = 2
model["root"]["input"]["solver"]["sections"]["section_times"] = [0.0, 60, 130]
model["root"]["input"]["solver"]["sections"]["section_continuity"] = [0]


# Set elements for connections
model["root"]["input"]["model"]["connections"] = OrderedDict()
model["root"]["input"]["model"]["connections"]["nswitches"] = 1
model["root"]["input"]["model"]["connections"]["switch_000"] = OrderedDict()
model["root"]["input"]["model"]["connections"]["switch_000"]["section"] = 0
model["root"]["input"]["model"]["connections"]["switch_000"]["connections"] = [0, 1, -1, -1, 2/60, 
                                                                               1, 2, -1, -1, 2/60]


# Set elements for user_solution_times
model["root"]["input"]["solver"]["user_solution_times"] = LinRange(0, 130, 130+1)

# Set elements for time_integrator
model["root"]["input"]["solver"]["time_integrator"] = OrderedDict()
model["root"]["input"]["solver"]["time_integrator"]["abstol"] = 1e-12
model["root"]["input"]["solver"]["time_integrator"]["algtol"] = 1e-10
model["root"]["input"]["solver"]["time_integrator"]["reltol"] = 1e-10



inlets, outlets, columns, switches, solverOptions = create_units(model)

using Sundials
solve_model_dae(
			columns = columns,
			switches = switches,
			solverOptions = solverOptions, 
			outlets = outlets, # Defaults to (0,) as output is also written to units 
			)


x0 = solverOptions.x0
differential_vars = ones(Int64,length(x0))
dx0 = zeros(Float64,length(x0))



#running simulations
for i = 1: length(switches.section_times) - 1 # corresponds to sections i=1

    # Set up parameter vector and empty elements 
    jacProto = nothing
    p_jac = nothing
    # analytical_jac = nothing
    fill!(dx0, 0.0)
    p = (columns, columns[1].RHS_q, columns[1].cpp, columns[1].qq, i, solverOptions.nColumns, solverOptions.idx_units, switches, p_jac)
    
    # If Analytical Jacobian == yes, set analytical Jacobian
    if solverOptions.analyticalJacobian == true
        # determine static jacobian and allocation matrices that are stored in p_jac
        p_jac = jac_static(columns[1],switches.ConnectionInstance.u_tot[switches.switchSetup[i], 1], p)
        p = (columns, columns[1].RHS_q, columns[1].cpp, columns[1].qq, i, solverOptions.nColumns, solverOptions.idx_units, switches, p_jac)
        analytical_jac = analytical_jac_dae! #refers to the function
    end

    # If jacobian prototype, compute at every section time as switches might change Jacobian 
    if solverOptions.prototypeJacobian == true
        
       # determine jacobian prototype
        jacProto = sparse(zeros(length(x0),length(x0)))
        analytical_jac(jacProto, solverOptions.x0 .+ 1e-6, solverOptions.x0 .+ 1e-6, p, 1e-7, 0.0)
        
        # set dq0dq to zero when computing SMA w. formulation 1 as dq/dt is not needed to be computed
        # This makes it slightly faster
        # if typeof(bind)==SMA 
        # 	@. @views jacProto[1 +columns[h].adsStride +columns[h].nComp*units[h].bindStride :columns[h].bindStride +columns[h].adsStride +columns[h].nComp*units[h].bindStride] = 0
        # end
    else
        # make jacProto empty such that it is not used
        jacProto = nothing
    end
    jj = zeros(length(x0),length(x0))
    analytical_jac_dae!(jj, x0, x0, p, 0, 0.0)
    
    # Update dx0 for the DAE for inlet 
    initialize_dae!(dx0, x0, p)
    
    # update the tspan and the inlets through i to the system
    tspan = (switches.section_times[i], switches.section_times[i+1])
    fun = DAEFunction(problemDAE!; jac_prototype = jacProto) #jac_prototype = jacProto, jac = analytical_jac_dae! # jacobian requires special definition, not implemented yet
    prob = DAEProblem(fun, dx0, x0, (0.0, tspan[2]-tspan[1]), p, differential_vars = differential_vars)
    sol = solve(prob, IDA(), saveat=solverOptions.solution_times, abstol=solverOptions.abstol, reltol=solverOptions.reltol) 
    
    #New initial conditions
    x0 = sol.u[end]
    
    #Extract solution in solution_outlet in each unit 
    for j = 1: solverOptions.nColumns
        for k = 1:columns[j].nComp 
            
            columns[j].solution_outlet[length(columns[j].solution_times) + 1 : length(columns[j].solution_times) + length(sol.t[2:end]), k] = sol(sol.t[2:end], idxs=k*columns[j].ConvDispOpInstance.nPoints + solverOptions.idx_units[j]).u
        end 
        append!(columns[j].solution_times, sol.t[2:end] .+ tspan[1])
    end

    # Write outlets - if specified 
    if outlets != (0,) 
        for j in eachindex(outlets)
            if outlets[j].idx_outlet != [-1]
                for k = 1:columns[1].nComp
                    
                    outlets[j].solution_outlet[length(outlets[j].solution_times) + 1 : length(outlets[j].solution_times) + length(sol.t[2:end]), k] = sol(sol.t[2:end], idxs=k*columns[outlets[j].idx_unit[switches.switchSetup[i]]].ConvDispOpInstance.nPoints + outlets[j].idx_outlet[switches.switchSetup[i]]).u
                end 
                append!(outlets[j].solution_times,sol.t[2:end] .+ tspan[1])
            end
        end
    end
    
    # Write to HDF5 using a function if relevant 
    
end