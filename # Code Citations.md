# Code Citations

## License: unknown
https://github.com/Kustra-Matt/Coevolutionary-Dynamics-Cryptic-Female-Choice/blob/652b72c57a5b0a6691927f8f72f885fedcc76d97/Running_Sims/RunModel.jl

```
## **Plan: GUI Progress Display + Simple Runner File**

### **Overview:**
Create a clean runner script with GUI toggle and delete old runner files, leaving only the new simplified runner.

---

### **Part 1: GUI Implementation in RunModel_KBuffer.jl**

**Approach:** Use Julia's built-in `Gtk` package for cross-platform GUI

**Changes needed:**
1. Add `using Gtk` to package imports (line ~18)
2. Add `show_gui=false` parameter to `sim()`, `runsim()`, `runsim_serial()` functions
3. Create GUI window initialization function:
   ```julia
   function create_progress_window()
     win = GtkWindow("Simulation Progress", 400, 150)
     label = GtkLabel("Initializing...")
     push!(win, label)
     showall(win)
     return win, label
   end
   ```
4. Update progress in generation loop:
   ```julia
   if show_gui && gen % 5 == 0  # Update every 5 generations
     set_gtk_property!(label, :label, "Generation: $gen/$generations\nPopulation: $(Nm_curr + Nf_curr)\nMales: $Nm_curr | Females: $Nf_curr")
     # Process GUI events to keep window responsive
     while Gtk.event_pending()
       Gtk.iterate()
     end
   end
   ```
5. Close GUI window after simulation completes

**Fallback:** If Gtk not available, print to console instead

---

### **Part 2: Create Simple Runner File**

**New file:** `run_kbuffer_simple.jl`

**Contents:**
```julia
# Simple Runner for RunModel_KBuffer.jl
# Edit parameters below and run: julia --project=@. run_kbuffer_simple.jl

# ========== EDITABLE PARAMETERS ==========
N = 1000              # Initial population size (males + females = 2*N)
generations = 100     # Number of generations to simulate
replicates = 1        # Number of replicate runs
K = N^2              # Carrying capacity (try: N^2, 5*N, 10*N, etc.)
maintain_sex_ratio = true   # true: 50/50 M/F split at K; false: random sampling
show_gui = false      # true: show GUI progress window; false: console only

# Other parameters (usually keep defaults)
mu = 5.0             # Mean trait value
var = 1.0            # Trait variance
a = 1.0              # Selection parameter
rsc = 0.25           # RSC parameter
tradeoff = true      # Enable tradeoff

# ========================================

# Run simulation
include("RunModel_KBuffer.jl")

using DataFrames, CSV, Dates

println("Starting K-buffer simulation...")
println("  N=$N, generations=$generations, replicates=$replicates")
println("  K=$K, maintain_sex_ratio=$maintain_sex_ratio")
println("  GUI display: $show_gui")

results = runsim_serial(replicates, N, mu, var, a, rsc, tradeoff, generations, -1, K, maintain_sex_ratio, show_gui)
data = DataFrame(results, [:MeanMale,:MeanFemale,:SDMale,:SDFemale,:cor,:MeanCount,:SDCount,:is,:int,:BMale,:GMale,:BFemale,:GFemale,:BSperm,:GSperm,:GMF,:GMS,:GFS,:a,:M
```


## License: unknown
https://github.com/Kustra-Matt/Coevolutionary-Dynamics-Cryptic-Female-Choice/blob/652b72c57a5b0a6691927f8f72f885fedcc76d97/Running_Sims/RunModel.jl

```
## **Plan: GUI Progress Display + Simple Runner File**

### **Overview:**
Create a clean runner script with GUI toggle and delete old runner files, leaving only the new simplified runner.

---

### **Part 1: GUI Implementation in RunModel_KBuffer.jl**

**Approach:** Use Julia's built-in `Gtk` package for cross-platform GUI

**Changes needed:**
1. Add `using Gtk` to package imports (line ~18)
2. Add `show_gui=false` parameter to `sim()`, `runsim()`, `runsim_serial()` functions
3. Create GUI window initialization function:
   ```julia
   function create_progress_window()
     win = GtkWindow("Simulation Progress", 400, 150)
     label = GtkLabel("Initializing...")
     push!(win, label)
     showall(win)
     return win, label
   end
   ```
4. Update progress in generation loop:
   ```julia
   if show_gui && gen % 5 == 0  # Update every 5 generations
     set_gtk_property!(label, :label, "Generation: $gen/$generations\nPopulation: $(Nm_curr + Nf_curr)\nMales: $Nm_curr | Females: $Nf_curr")
     # Process GUI events to keep window responsive
     while Gtk.event_pending()
       Gtk.iterate()
     end
   end
   ```
5. Close GUI window after simulation completes

**Fallback:** If Gtk not available, print to console instead

---

### **Part 2: Create Simple Runner File**

**New file:** `run_kbuffer_simple.jl`

**Contents:**
```julia
# Simple Runner for RunModel_KBuffer.jl
# Edit parameters below and run: julia --project=@. run_kbuffer_simple.jl

# ========== EDITABLE PARAMETERS ==========
N = 1000              # Initial population size (males + females = 2*N)
generations = 100     # Number of generations to simulate
replicates = 1        # Number of replicate runs
K = N^2              # Carrying capacity (try: N^2, 5*N, 10*N, etc.)
maintain_sex_ratio = true   # true: 50/50 M/F split at K; false: random sampling
show_gui = false      # true: show GUI progress window; false: console only

# Other parameters (usually keep defaults)
mu = 5.0             # Mean trait value
var = 1.0            # Trait variance
a = 1.0              # Selection parameter
rsc = 0.25           # RSC parameter
tradeoff = true      # Enable tradeoff

# ========================================

# Run simulation
include("RunModel_KBuffer.jl")

using DataFrames, CSV, Dates

println("Starting K-buffer simulation...")
println("  N=$N, generations=$generations, replicates=$replicates")
println("  K=$K, maintain_sex_ratio=$maintain_sex_ratio")
println("  GUI display: $show_gui")

results = runsim_serial(replicates, N, mu, var, a, rsc, tradeoff, generations, -1, K, maintain_sex_ratio, show_gui)
data = DataFrame(results, [:MeanMale,:MeanFemale,:SDMale,:SDFemale,:cor,:MeanCount,:SDCount,:is,:int,:BMale,:GMale,:BFemale,:GFemale,:BSperm,:GSperm,:GMF,:GMS,:GFS,:a,:M
```


## License: unknown
https://github.com/Kustra-Matt/Coevolutionary-Dynamics-Cryptic-Female-Choice/blob/652b72c57a5b0a6691927f8f72f885fedcc76d97/Running_Sims/RunModel.jl

```
## **Plan: GUI Progress Display + Simple Runner File**

### **Overview:**
Create a clean runner script with GUI toggle and delete old runner files, leaving only the new simplified runner.

---

### **Part 1: GUI Implementation in RunModel_KBuffer.jl**

**Approach:** Use Julia's built-in `Gtk` package for cross-platform GUI

**Changes needed:**
1. Add `using Gtk` to package imports (line ~18)
2. Add `show_gui=false` parameter to `sim()`, `runsim()`, `runsim_serial()` functions
3. Create GUI window initialization function:
   ```julia
   function create_progress_window()
     win = GtkWindow("Simulation Progress", 400, 150)
     label = GtkLabel("Initializing...")
     push!(win, label)
     showall(win)
     return win, label
   end
   ```
4. Update progress in generation loop:
   ```julia
   if show_gui && gen % 5 == 0  # Update every 5 generations
     set_gtk_property!(label, :label, "Generation: $gen/$generations\nPopulation: $(Nm_curr + Nf_curr)\nMales: $Nm_curr | Females: $Nf_curr")
     # Process GUI events to keep window responsive
     while Gtk.event_pending()
       Gtk.iterate()
     end
   end
   ```
5. Close GUI window after simulation completes

**Fallback:** If Gtk not available, print to console instead

---

### **Part 2: Create Simple Runner File**

**New file:** `run_kbuffer_simple.jl`

**Contents:**
```julia
# Simple Runner for RunModel_KBuffer.jl
# Edit parameters below and run: julia --project=@. run_kbuffer_simple.jl

# ========== EDITABLE PARAMETERS ==========
N = 1000              # Initial population size (males + females = 2*N)
generations = 100     # Number of generations to simulate
replicates = 1        # Number of replicate runs
K = N^2              # Carrying capacity (try: N^2, 5*N, 10*N, etc.)
maintain_sex_ratio = true   # true: 50/50 M/F split at K; false: random sampling
show_gui = false      # true: show GUI progress window; false: console only

# Other parameters (usually keep defaults)
mu = 5.0             # Mean trait value
var = 1.0            # Trait variance
a = 1.0              # Selection parameter
rsc = 0.25           # RSC parameter
tradeoff = true      # Enable tradeoff

# ========================================

# Run simulation
include("RunModel_KBuffer.jl")

using DataFrames, CSV, Dates

println("Starting K-buffer simulation...")
println("  N=$N, generations=$generations, replicates=$replicates")
println("  K=$K, maintain_sex_ratio=$maintain_sex_ratio")
println("  GUI display: $show_gui")

results = runsim_serial(replicates, N, mu, var, a, rsc, tradeoff, generations, -1, K, maintain_sex_ratio, show_gui)
data = DataFrame(results, [:MeanMale,:MeanFemale,:SDMale,:SDFemale,:cor,:MeanCount,:SDCount,:is,:int,:BMale,:GMale,:BFemale,:GFemale,:BSperm,:GSperm,:GMF,:GMS,:GFS,:a,:M
```


## License: unknown
https://github.com/Kustra-Matt/Coevolutionary-Dynamics-Cryptic-Female-Choice/blob/652b72c57a5b0a6691927f8f72f885fedcc76d97/Running_Sims/RunModel.jl

```
## **Plan: GUI Progress Display + Simple Runner File**

### **Overview:**
Create a clean runner script with GUI toggle and delete old runner files, leaving only the new simplified runner.

---

### **Part 1: GUI Implementation in RunModel_KBuffer.jl**

**Approach:** Use Julia's built-in `Gtk` package for cross-platform GUI

**Changes needed:**
1. Add `using Gtk` to package imports (line ~18)
2. Add `show_gui=false` parameter to `sim()`, `runsim()`, `runsim_serial()` functions
3. Create GUI window initialization function:
   ```julia
   function create_progress_window()
     win = GtkWindow("Simulation Progress", 400, 150)
     label = GtkLabel("Initializing...")
     push!(win, label)
     showall(win)
     return win, label
   end
   ```
4. Update progress in generation loop:
   ```julia
   if show_gui && gen % 5 == 0  # Update every 5 generations
     set_gtk_property!(label, :label, "Generation: $gen/$generations\nPopulation: $(Nm_curr + Nf_curr)\nMales: $Nm_curr | Females: $Nf_curr")
     # Process GUI events to keep window responsive
     while Gtk.event_pending()
       Gtk.iterate()
     end
   end
   ```
5. Close GUI window after simulation completes

**Fallback:** If Gtk not available, print to console instead

---

### **Part 2: Create Simple Runner File**

**New file:** `run_kbuffer_simple.jl`

**Contents:**
```julia
# Simple Runner for RunModel_KBuffer.jl
# Edit parameters below and run: julia --project=@. run_kbuffer_simple.jl

# ========== EDITABLE PARAMETERS ==========
N = 1000              # Initial population size (males + females = 2*N)
generations = 100     # Number of generations to simulate
replicates = 1        # Number of replicate runs
K = N^2              # Carrying capacity (try: N^2, 5*N, 10*N, etc.)
maintain_sex_ratio = true   # true: 50/50 M/F split at K; false: random sampling
show_gui = false      # true: show GUI progress window; false: console only

# Other parameters (usually keep defaults)
mu = 5.0             # Mean trait value
var = 1.0            # Trait variance
a = 1.0              # Selection parameter
rsc = 0.25           # RSC parameter
tradeoff = true      # Enable tradeoff

# ========================================

# Run simulation
include("RunModel_KBuffer.jl")

using DataFrames, CSV, Dates

println("Starting K-buffer simulation...")
println("  N=$N, generations=$generations, replicates=$replicates")
println("  K=$K, maintain_sex_ratio=$maintain_sex_ratio")
println("  GUI display: $show_gui")

results = runsim_serial(replicates, N, mu, var, a, rsc, tradeoff, generations, -1, K, maintain_sex_ratio, show_gui)
data = DataFrame(results, [:MeanMale,:MeanFemale,:SDMale,:SDFemale,:cor,:MeanCount,:SDCount,:is,:int,:BMale,:GMale,:BFemale,:GFemale,:BSperm,:GSperm,:GMF,:GMS,:GFS,:a,:M
```


## License: unknown
https://github.com/Kustra-Matt/Coevolutionary-Dynamics-Cryptic-Female-Choice/blob/652b72c57a5b0a6691927f8f72f885fedcc76d97/Running_Sims/RunModel.jl

```
## **Plan: GUI Progress Display + Simple Runner File**

### **Overview:**
Create a clean runner script with GUI toggle and delete old runner files, leaving only the new simplified runner.

---

### **Part 1: GUI Implementation in RunModel_KBuffer.jl**

**Approach:** Use Julia's built-in `Gtk` package for cross-platform GUI

**Changes needed:**
1. Add `using Gtk` to package imports (line ~18)
2. Add `show_gui=false` parameter to `sim()`, `runsim()`, `runsim_serial()` functions
3. Create GUI window initialization function:
   ```julia
   function create_progress_window()
     win = GtkWindow("Simulation Progress", 400, 150)
     label = GtkLabel("Initializing...")
     push!(win, label)
     showall(win)
     return win, label
   end
   ```
4. Update progress in generation loop:
   ```julia
   if show_gui && gen % 5 == 0  # Update every 5 generations
     set_gtk_property!(label, :label, "Generation: $gen/$generations\nPopulation: $(Nm_curr + Nf_curr)\nMales: $Nm_curr | Females: $Nf_curr")
     # Process GUI events to keep window responsive
     while Gtk.event_pending()
       Gtk.iterate()
     end
   end
   ```
5. Close GUI window after simulation completes

**Fallback:** If Gtk not available, print to console instead

---

### **Part 2: Create Simple Runner File**

**New file:** `run_kbuffer_simple.jl`

**Contents:**
```julia
# Simple Runner for RunModel_KBuffer.jl
# Edit parameters below and run: julia --project=@. run_kbuffer_simple.jl

# ========== EDITABLE PARAMETERS ==========
N = 1000              # Initial population size (males + females = 2*N)
generations = 100     # Number of generations to simulate
replicates = 1        # Number of replicate runs
K = N^2              # Carrying capacity (try: N^2, 5*N, 10*N, etc.)
maintain_sex_ratio = true   # true: 50/50 M/F split at K; false: random sampling
show_gui = false      # true: show GUI progress window; false: console only

# Other parameters (usually keep defaults)
mu = 5.0             # Mean trait value
var = 1.0            # Trait variance
a = 1.0              # Selection parameter
rsc = 0.25           # RSC parameter
tradeoff = true      # Enable tradeoff

# ========================================

# Run simulation
include("RunModel_KBuffer.jl")

using DataFrames, CSV, Dates

println("Starting K-buffer simulation...")
println("  N=$N, generations=$generations, replicates=$replicates")
println("  K=$K, maintain_sex_ratio=$maintain_sex_ratio")
println("  GUI display: $show_gui")

results = runsim_serial(replicates, N, mu, var, a, rsc, tradeoff, generations, -1, K, maintain_sex_ratio, show_gui)
data = DataFrame(results, [:MeanMale,:MeanFemale,:SDMale,:SDFemale,:cor,:MeanCount,:SDCount,:is,:int,:BMale,:GMale,:BFemale,:GFemale,:BSperm,:GSperm,:GMF,:GMS,:GFS,:a,:M
```


## License: unknown
https://github.com/Kustra-Matt/Coevolutionary-Dynamics-Cryptic-Female-Choice/blob/652b72c57a5b0a6691927f8f72f885fedcc76d97/Running_Sims/RunModel.jl

```
## **Plan: GUI Progress Display + Simple Runner File**

### **Overview:**
Create a clean runner script with GUI toggle and delete old runner files, leaving only the new simplified runner.

---

### **Part 1: GUI Implementation in RunModel_KBuffer.jl**

**Approach:** Use Julia's built-in `Gtk` package for cross-platform GUI

**Changes needed:**
1. Add `using Gtk` to package imports (line ~18)
2. Add `show_gui=false` parameter to `sim()`, `runsim()`, `runsim_serial()` functions
3. Create GUI window initialization function:
   ```julia
   function create_progress_window()
     win = GtkWindow("Simulation Progress", 400, 150)
     label = GtkLabel("Initializing...")
     push!(win, label)
     showall(win)
     return win, label
   end
   ```
4. Update progress in generation loop:
   ```julia
   if show_gui && gen % 5 == 0  # Update every 5 generations
     set_gtk_property!(label, :label, "Generation: $gen/$generations\nPopulation: $(Nm_curr + Nf_curr)\nMales: $Nm_curr | Females: $Nf_curr")
     # Process GUI events to keep window responsive
     while Gtk.event_pending()
       Gtk.iterate()
     end
   end
   ```
5. Close GUI window after simulation completes

**Fallback:** If Gtk not available, print to console instead

---

### **Part 2: Create Simple Runner File**

**New file:** `run_kbuffer_simple.jl`

**Contents:**
```julia
# Simple Runner for RunModel_KBuffer.jl
# Edit parameters below and run: julia --project=@. run_kbuffer_simple.jl

# ========== EDITABLE PARAMETERS ==========
N = 1000              # Initial population size (males + females = 2*N)
generations = 100     # Number of generations to simulate
replicates = 1        # Number of replicate runs
K = N^2              # Carrying capacity (try: N^2, 5*N, 10*N, etc.)
maintain_sex_ratio = true   # true: 50/50 M/F split at K; false: random sampling
show_gui = false      # true: show GUI progress window; false: console only

# Other parameters (usually keep defaults)
mu = 5.0             # Mean trait value
var = 1.0            # Trait variance
a = 1.0              # Selection parameter
rsc = 0.25           # RSC parameter
tradeoff = true      # Enable tradeoff

# ========================================

# Run simulation
include("RunModel_KBuffer.jl")

using DataFrames, CSV, Dates

println("Starting K-buffer simulation...")
println("  N=$N, generations=$generations, replicates=$replicates")
println("  K=$K, maintain_sex_ratio=$maintain_sex_ratio")
println("  GUI display: $show_gui")

results = runsim_serial(replicates, N, mu, var, a, rsc, tradeoff, generations, -1, K, maintain_sex_ratio, show_gui)
data = DataFrame(results, [:MeanMale,:MeanFemale,:SDMale,:SDFemale,:cor,:MeanCount,:SDCount,:is,:int,:BMale,:GMale,:BFemale,:GFemale,:BSperm,:GSperm,:GMF,:GMS,:GFS,:a,:M
```


## License: unknown
https://github.com/Kustra-Matt/Coevolutionary-Dynamics-Cryptic-Female-Choice/blob/652b72c57a5b0a6691927f8f72f885fedcc76d97/Running_Sims/RunModel.jl

```
## **Plan: GUI Progress Display + Simple Runner File**

### **Overview:**
Create a clean runner script with GUI toggle and delete old runner files, leaving only the new simplified runner.

---

### **Part 1: GUI Implementation in RunModel_KBuffer.jl**

**Approach:** Use Julia's built-in `Gtk` package for cross-platform GUI

**Changes needed:**
1. Add `using Gtk` to package imports (line ~18)
2. Add `show_gui=false` parameter to `sim()`, `runsim()`, `runsim_serial()` functions
3. Create GUI window initialization function:
   ```julia
   function create_progress_window()
     win = GtkWindow("Simulation Progress", 400, 150)
     label = GtkLabel("Initializing...")
     push!(win, label)
     showall(win)
     return win, label
   end
   ```
4. Update progress in generation loop:
   ```julia
   if show_gui && gen % 5 == 0  # Update every 5 generations
     set_gtk_property!(label, :label, "Generation: $gen/$generations\nPopulation: $(Nm_curr + Nf_curr)\nMales: $Nm_curr | Females: $Nf_curr")
     # Process GUI events to keep window responsive
     while Gtk.event_pending()
       Gtk.iterate()
     end
   end
   ```
5. Close GUI window after simulation completes

**Fallback:** If Gtk not available, print to console instead

---

### **Part 2: Create Simple Runner File**

**New file:** `run_kbuffer_simple.jl`

**Contents:**
```julia
# Simple Runner for RunModel_KBuffer.jl
# Edit parameters below and run: julia --project=@. run_kbuffer_simple.jl

# ========== EDITABLE PARAMETERS ==========
N = 1000              # Initial population size (males + females = 2*N)
generations = 100     # Number of generations to simulate
replicates = 1        # Number of replicate runs
K = N^2              # Carrying capacity (try: N^2, 5*N, 10*N, etc.)
maintain_sex_ratio = true   # true: 50/50 M/F split at K; false: random sampling
show_gui = false      # true: show GUI progress window; false: console only

# Other parameters (usually keep defaults)
mu = 5.0             # Mean trait value
var = 1.0            # Trait variance
a = 1.0              # Selection parameter
rsc = 0.25           # RSC parameter
tradeoff = true      # Enable tradeoff

# ========================================

# Run simulation
include("RunModel_KBuffer.jl")

using DataFrames, CSV, Dates

println("Starting K-buffer simulation...")
println("  N=$N, generations=$generations, replicates=$replicates")
println("  K=$K, maintain_sex_ratio=$maintain_sex_ratio")
println("  GUI display: $show_gui")

results = runsim_serial(replicates, N, mu, var, a, rsc, tradeoff, generations, -1, K, maintain_sex_ratio, show_gui)
data = DataFrame(results, [:MeanMale,:MeanFemale,:SDMale,:SDFemale,:cor,:MeanCount,:SDCount,:is,:int,:BMale,:GMale,:BFemale,:GFemale,:BSperm,:GSperm,:GMF,:GMS,:GFS,:a,:M
```


## License: unknown
https://github.com/Kustra-Matt/Coevolutionary-Dynamics-Cryptic-Female-Choice/blob/652b72c57a5b0a6691927f8f72f885fedcc76d97/Running_Sims/RunModel.jl

```
## **Plan: GUI Progress Display + Simple Runner File**

### **Overview:**
Create a clean runner script with GUI toggle and delete old runner files, leaving only the new simplified runner.

---

### **Part 1: GUI Implementation in RunModel_KBuffer.jl**

**Approach:** Use Julia's built-in `Gtk` package for cross-platform GUI

**Changes needed:**
1. Add `using Gtk` to package imports (line ~18)
2. Add `show_gui=false` parameter to `sim()`, `runsim()`, `runsim_serial()` functions
3. Create GUI window initialization function:
   ```julia
   function create_progress_window()
     win = GtkWindow("Simulation Progress", 400, 150)
     label = GtkLabel("Initializing...")
     push!(win, label)
     showall(win)
     return win, label
   end
   ```
4. Update progress in generation loop:
   ```julia
   if show_gui && gen % 5 == 0  # Update every 5 generations
     set_gtk_property!(label, :label, "Generation: $gen/$generations\nPopulation: $(Nm_curr + Nf_curr)\nMales: $Nm_curr | Females: $Nf_curr")
     # Process GUI events to keep window responsive
     while Gtk.event_pending()
       Gtk.iterate()
     end
   end
   ```
5. Close GUI window after simulation completes

**Fallback:** If Gtk not available, print to console instead

---

### **Part 2: Create Simple Runner File**

**New file:** `run_kbuffer_simple.jl`

**Contents:**
```julia
# Simple Runner for RunModel_KBuffer.jl
# Edit parameters below and run: julia --project=@. run_kbuffer_simple.jl

# ========== EDITABLE PARAMETERS ==========
N = 1000              # Initial population size (males + females = 2*N)
generations = 100     # Number of generations to simulate
replicates = 1        # Number of replicate runs
K = N^2              # Carrying capacity (try: N^2, 5*N, 10*N, etc.)
maintain_sex_ratio = true   # true: 50/50 M/F split at K; false: random sampling
show_gui = false      # true: show GUI progress window; false: console only

# Other parameters (usually keep defaults)
mu = 5.0             # Mean trait value
var = 1.0            # Trait variance
a = 1.0              # Selection parameter
rsc = 0.25           # RSC parameter
tradeoff = true      # Enable tradeoff

# ========================================

# Run simulation
include("RunModel_KBuffer.jl")

using DataFrames, CSV, Dates

println("Starting K-buffer simulation...")
println("  N=$N, generations=$generations, replicates=$replicates")
println("  K=$K, maintain_sex_ratio=$maintain_sex_ratio")
println("  GUI display: $show_gui")

results = runsim_serial(replicates, N, mu, var, a, rsc, tradeoff, generations, -1, K, maintain_sex_ratio, show_gui)
data = DataFrame(results, [:MeanMale,:MeanFemale,:SDMale,:SDFemale,:cor,:MeanCount,:SDCount,:is,:int,:BMale,:GMale,:BFemale,:GFemale,:BSperm,:GSperm,:GMF,:GMS,:GFS,:a,:M
```


## License: unknown
https://github.com/Kustra-Matt/Coevolutionary-Dynamics-Cryptic-Female-Choice/blob/652b72c57a5b0a6691927f8f72f885fedcc76d97/Running_Sims/RunModel.jl

```
## **Plan: GUI Progress Display + Simple Runner File**

### **Overview:**
Create a clean runner script with GUI toggle and delete old runner files, leaving only the new simplified runner.

---

### **Part 1: GUI Implementation in RunModel_KBuffer.jl**

**Approach:** Use Julia's built-in `Gtk` package for cross-platform GUI

**Changes needed:**
1. Add `using Gtk` to package imports (line ~18)
2. Add `show_gui=false` parameter to `sim()`, `runsim()`, `runsim_serial()` functions
3. Create GUI window initialization function:
   ```julia
   function create_progress_window()
     win = GtkWindow("Simulation Progress", 400, 150)
     label = GtkLabel("Initializing...")
     push!(win, label)
     showall(win)
     return win, label
   end
   ```
4. Update progress in generation loop:
   ```julia
   if show_gui && gen % 5 == 0  # Update every 5 generations
     set_gtk_property!(label, :label, "Generation: $gen/$generations\nPopulation: $(Nm_curr + Nf_curr)\nMales: $Nm_curr | Females: $Nf_curr")
     # Process GUI events to keep window responsive
     while Gtk.event_pending()
       Gtk.iterate()
     end
   end
   ```
5. Close GUI window after simulation completes

**Fallback:** If Gtk not available, print to console instead

---

### **Part 2: Create Simple Runner File**

**New file:** `run_kbuffer_simple.jl`

**Contents:**
```julia
# Simple Runner for RunModel_KBuffer.jl
# Edit parameters below and run: julia --project=@. run_kbuffer_simple.jl

# ========== EDITABLE PARAMETERS ==========
N = 1000              # Initial population size (males + females = 2*N)
generations = 100     # Number of generations to simulate
replicates = 1        # Number of replicate runs
K = N^2              # Carrying capacity (try: N^2, 5*N, 10*N, etc.)
maintain_sex_ratio = true   # true: 50/50 M/F split at K; false: random sampling
show_gui = false      # true: show GUI progress window; false: console only

# Other parameters (usually keep defaults)
mu = 5.0             # Mean trait value
var = 1.0            # Trait variance
a = 1.0              # Selection parameter
rsc = 0.25           # RSC parameter
tradeoff = true      # Enable tradeoff

# ========================================

# Run simulation
include("RunModel_KBuffer.jl")

using DataFrames, CSV, Dates

println("Starting K-buffer simulation...")
println("  N=$N, generations=$generations, replicates=$replicates")
println("  K=$K, maintain_sex_ratio=$maintain_sex_ratio")
println("  GUI display: $show_gui")

results = runsim_serial(replicates, N, mu, var, a, rsc, tradeoff, generations, -1, K, maintain_sex_ratio, show_gui)
data = DataFrame(results, [:MeanMale,:MeanFemale,:SDMale,:SDFemale,:cor,:MeanCount,:SDCount,:is,:int,:BMale,:GMale,:BFemale,:GFemale,:BSperm,:GSperm,:GMF,:GMS,:GFS,:a,:M
```


## License: unknown
https://github.com/Kustra-Matt/Coevolutionary-Dynamics-Cryptic-Female-Choice/blob/652b72c57a5b0a6691927f8f72f885fedcc76d97/Running_Sims/RunModel.jl

```
## **Plan: GUI Progress Display + Simple Runner File**

### **Overview:**
Create a clean runner script with GUI toggle and delete old runner files, leaving only the new simplified runner.

---

### **Part 1: GUI Implementation in RunModel_KBuffer.jl**

**Approach:** Use Julia's built-in `Gtk` package for cross-platform GUI

**Changes needed:**
1. Add `using Gtk` to package imports (line ~18)
2. Add `show_gui=false` parameter to `sim()`, `runsim()`, `runsim_serial()` functions
3. Create GUI window initialization function:
   ```julia
   function create_progress_window()
     win = GtkWindow("Simulation Progress", 400, 150)
     label = GtkLabel("Initializing...")
     push!(win, label)
     showall(win)
     return win, label
   end
   ```
4. Update progress in generation loop:
   ```julia
   if show_gui && gen % 5 == 0  # Update every 5 generations
     set_gtk_property!(label, :label, "Generation: $gen/$generations\nPopulation: $(Nm_curr + Nf_curr)\nMales: $Nm_curr | Females: $Nf_curr")
     # Process GUI events to keep window responsive
     while Gtk.event_pending()
       Gtk.iterate()
     end
   end
   ```
5. Close GUI window after simulation completes

**Fallback:** If Gtk not available, print to console instead

---

### **Part 2: Create Simple Runner File**

**New file:** `run_kbuffer_simple.jl`

**Contents:**
```julia
# Simple Runner for RunModel_KBuffer.jl
# Edit parameters below and run: julia --project=@. run_kbuffer_simple.jl

# ========== EDITABLE PARAMETERS ==========
N = 1000              # Initial population size (males + females = 2*N)
generations = 100     # Number of generations to simulate
replicates = 1        # Number of replicate runs
K = N^2              # Carrying capacity (try: N^2, 5*N, 10*N, etc.)
maintain_sex_ratio = true   # true: 50/50 M/F split at K; false: random sampling
show_gui = false      # true: show GUI progress window; false: console only

# Other parameters (usually keep defaults)
mu = 5.0             # Mean trait value
var = 1.0            # Trait variance
a = 1.0              # Selection parameter
rsc = 0.25           # RSC parameter
tradeoff = true      # Enable tradeoff

# ========================================

# Run simulation
include("RunModel_KBuffer.jl")

using DataFrames, CSV, Dates

println("Starting K-buffer simulation...")
println("  N=$N, generations=$generations, replicates=$replicates")
println("  K=$K, maintain_sex_ratio=$maintain_sex_ratio")
println("  GUI display: $show_gui")

results = runsim_serial(replicates, N, mu, var, a, rsc, tradeoff, generations, -1, K, maintain_sex_ratio, show_gui)
data = DataFrame(results, [:MeanMale,:MeanFemale,:SDMale,:SDFemale,:cor,:MeanCount,:SDCount,:is,:int,:BMale,:GMale,:BFemale,:GFemale,:BSperm,:GSperm,:GMF,:GMS,:GFS,:a,:M
```


## License: unknown
https://github.com/Kustra-Matt/Coevolutionary-Dynamics-Cryptic-Female-Choice/blob/652b72c57a5b0a6691927f8f72f885fedcc76d97/Running_Sims/RunModel.jl

```
## **Plan: GUI Progress Display + Simple Runner File**

### **Overview:**
Create a clean runner script with GUI toggle and delete old runner files, leaving only the new simplified runner.

---

### **Part 1: GUI Implementation in RunModel_KBuffer.jl**

**Approach:** Use Julia's built-in `Gtk` package for cross-platform GUI

**Changes needed:**
1. Add `using Gtk` to package imports (line ~18)
2. Add `show_gui=false` parameter to `sim()`, `runsim()`, `runsim_serial()` functions
3. Create GUI window initialization function:
   ```julia
   function create_progress_window()
     win = GtkWindow("Simulation Progress", 400, 150)
     label = GtkLabel("Initializing...")
     push!(win, label)
     showall(win)
     return win, label
   end
   ```
4. Update progress in generation loop:
   ```julia
   if show_gui && gen % 5 == 0  # Update every 5 generations
     set_gtk_property!(label, :label, "Generation: $gen/$generations\nPopulation: $(Nm_curr + Nf_curr)\nMales: $Nm_curr | Females: $Nf_curr")
     # Process GUI events to keep window responsive
     while Gtk.event_pending()
       Gtk.iterate()
     end
   end
   ```
5. Close GUI window after simulation completes

**Fallback:** If Gtk not available, print to console instead

---

### **Part 2: Create Simple Runner File**

**New file:** `run_kbuffer_simple.jl`

**Contents:**
```julia
# Simple Runner for RunModel_KBuffer.jl
# Edit parameters below and run: julia --project=@. run_kbuffer_simple.jl

# ========== EDITABLE PARAMETERS ==========
N = 1000              # Initial population size (males + females = 2*N)
generations = 100     # Number of generations to simulate
replicates = 1        # Number of replicate runs
K = N^2              # Carrying capacity (try: N^2, 5*N, 10*N, etc.)
maintain_sex_ratio = true   # true: 50/50 M/F split at K; false: random sampling
show_gui = false      # true: show GUI progress window; false: console only

# Other parameters (usually keep defaults)
mu = 5.0             # Mean trait value
var = 1.0            # Trait variance
a = 1.0              # Selection parameter
rsc = 0.25           # RSC parameter
tradeoff = true      # Enable tradeoff

# ========================================

# Run simulation
include("RunModel_KBuffer.jl")

using DataFrames, CSV, Dates

println("Starting K-buffer simulation...")
println("  N=$N, generations=$generations, replicates=$replicates")
println("  K=$K, maintain_sex_ratio=$maintain_sex_ratio")
println("  GUI display: $show_gui")

results = runsim_serial(replicates, N, mu, var, a, rsc, tradeoff, generations, -1, K, maintain_sex_ratio, show_gui)
data = DataFrame(results, [:MeanMale,:MeanFemale,:SDMale,:SDFemale,:cor,:MeanCount,:SDCount,:is,:int,:BMale,:GMale,:BFemale,:GFemale,:BSperm,:GSperm,:GMF,:GMS,:GFS,:a,:M
```


## License: unknown
https://github.com/Kustra-Matt/Coevolutionary-Dynamics-Cryptic-Female-Choice/blob/652b72c57a5b0a6691927f8f72f885fedcc76d97/Running_Sims/RunModel.jl

```
## **Plan: GUI Progress Display + Simple Runner File**

### **Overview:**
Create a clean runner script with GUI toggle and delete old runner files, leaving only the new simplified runner.

---

### **Part 1: GUI Implementation in RunModel_KBuffer.jl**

**Approach:** Use Julia's built-in `Gtk` package for cross-platform GUI

**Changes needed:**
1. Add `using Gtk` to package imports (line ~18)
2. Add `show_gui=false` parameter to `sim()`, `runsim()`, `runsim_serial()` functions
3. Create GUI window initialization function:
   ```julia
   function create_progress_window()
     win = GtkWindow("Simulation Progress", 400, 150)
     label = GtkLabel("Initializing...")
     push!(win, label)
     showall(win)
     return win, label
   end
   ```
4. Update progress in generation loop:
   ```julia
   if show_gui && gen % 5 == 0  # Update every 5 generations
     set_gtk_property!(label, :label, "Generation: $gen/$generations\nPopulation: $(Nm_curr + Nf_curr)\nMales: $Nm_curr | Females: $Nf_curr")
     # Process GUI events to keep window responsive
     while Gtk.event_pending()
       Gtk.iterate()
     end
   end
   ```
5. Close GUI window after simulation completes

**Fallback:** If Gtk not available, print to console instead

---

### **Part 2: Create Simple Runner File**

**New file:** `run_kbuffer_simple.jl`

**Contents:**
```julia
# Simple Runner for RunModel_KBuffer.jl
# Edit parameters below and run: julia --project=@. run_kbuffer_simple.jl

# ========== EDITABLE PARAMETERS ==========
N = 1000              # Initial population size (males + females = 2*N)
generations = 100     # Number of generations to simulate
replicates = 1        # Number of replicate runs
K = N^2              # Carrying capacity (try: N^2, 5*N, 10*N, etc.)
maintain_sex_ratio = true   # true: 50/50 M/F split at K; false: random sampling
show_gui = false      # true: show GUI progress window; false: console only

# Other parameters (usually keep defaults)
mu = 5.0             # Mean trait value
var = 1.0            # Trait variance
a = 1.0              # Selection parameter
rsc = 0.25           # RSC parameter
tradeoff = true      # Enable tradeoff

# ========================================

# Run simulation
include("RunModel_KBuffer.jl")

using DataFrames, CSV, Dates

println("Starting K-buffer simulation...")
println("  N=$N, generations=$generations, replicates=$replicates")
println("  K=$K, maintain_sex_ratio=$maintain_sex_ratio")
println("  GUI display: $show_gui")

results = runsim_serial(replicates, N, mu, var, a, rsc, tradeoff, generations, -1, K, maintain_sex_ratio, show_gui)
data = DataFrame(results, [:MeanMale,:MeanFemale,:SDMale,:SDFemale,:cor,:MeanCount,:SDCount,:is,:int,:BMale,:GMale,:BFemale,:GFemale,:BSperm,:GSperm,:GMF,:GMS,:GFS,:a,:M
```


## License: unknown
https://github.com/Kustra-Matt/Coevolutionary-Dynamics-Cryptic-Female-Choice/blob/652b72c57a5b0a6691927f8f72f885fedcc76d97/Running_Sims/RunModel.jl

```
## **Plan: GUI Progress Display + Simple Runner File**

### **Overview:**
Create a clean runner script with GUI toggle and delete old runner files, leaving only the new simplified runner.

---

### **Part 1: GUI Implementation in RunModel_KBuffer.jl**

**Approach:** Use Julia's built-in `Gtk` package for cross-platform GUI

**Changes needed:**
1. Add `using Gtk` to package imports (line ~18)
2. Add `show_gui=false` parameter to `sim()`, `runsim()`, `runsim_serial()` functions
3. Create GUI window initialization function:
   ```julia
   function create_progress_window()
     win = GtkWindow("Simulation Progress", 400, 150)
     label = GtkLabel("Initializing...")
     push!(win, label)
     showall(win)
     return win, label
   end
   ```
4. Update progress in generation loop:
   ```julia
   if show_gui && gen % 5 == 0  # Update every 5 generations
     set_gtk_property!(label, :label, "Generation: $gen/$generations\nPopulation: $(Nm_curr + Nf_curr)\nMales: $Nm_curr | Females: $Nf_curr")
     # Process GUI events to keep window responsive
     while Gtk.event_pending()
       Gtk.iterate()
     end
   end
   ```
5. Close GUI window after simulation completes

**Fallback:** If Gtk not available, print to console instead

---

### **Part 2: Create Simple Runner File**

**New file:** `run_kbuffer_simple.jl`

**Contents:**
```julia
# Simple Runner for RunModel_KBuffer.jl
# Edit parameters below and run: julia --project=@. run_kbuffer_simple.jl

# ========== EDITABLE PARAMETERS ==========
N = 1000              # Initial population size (males + females = 2*N)
generations = 100     # Number of generations to simulate
replicates = 1        # Number of replicate runs
K = N^2              # Carrying capacity (try: N^2, 5*N, 10*N, etc.)
maintain_sex_ratio = true   # true: 50/50 M/F split at K; false: random sampling
show_gui = false      # true: show GUI progress window; false: console only

# Other parameters (usually keep defaults)
mu = 5.0             # Mean trait value
var = 1.0            # Trait variance
a = 1.0              # Selection parameter
rsc = 0.25           # RSC parameter
tradeoff = true      # Enable tradeoff

# ========================================

# Run simulation
include("RunModel_KBuffer.jl")

using DataFrames, CSV, Dates

println("Starting K-buffer simulation...")
println("  N=$N, generations=$generations, replicates=$replicates")
println("  K=$K, maintain_sex_ratio=$maintain_sex_ratio")
println("  GUI display: $show_gui")

results = runsim_serial(replicates, N, mu, var, a, rsc, tradeoff, generations, -1, K, maintain_sex_ratio, show_gui)
data = DataFrame(results, [:MeanMale,:MeanFemale,:SDMale,:SDFemale,:cor,:MeanCount,:SDCount,:is,:int,:BMale,:GMale,:BFemale,:GFemale,:BSperm,:GSperm,:GMF,:GMS,:GFS,:a,:M
```


## License: unknown
https://github.com/Kustra-Matt/Coevolutionary-Dynamics-Cryptic-Female-Choice/blob/652b72c57a5b0a6691927f8f72f885fedcc76d97/Running_Sims/RunModel.jl

```
## **Plan: GUI Progress Display + Simple Runner File**

### **Overview:**
Create a clean runner script with GUI toggle and delete old runner files, leaving only the new simplified runner.

---

### **Part 1: GUI Implementation in RunModel_KBuffer.jl**

**Approach:** Use Julia's built-in `Gtk` package for cross-platform GUI

**Changes needed:**
1. Add `using Gtk` to package imports (line ~18)
2. Add `show_gui=false` parameter to `sim()`, `runsim()`, `runsim_serial()` functions
3. Create GUI window initialization function:
   ```julia
   function create_progress_window()
     win = GtkWindow("Simulation Progress", 400, 150)
     label = GtkLabel("Initializing...")
     push!(win, label)
     showall(win)
     return win, label
   end
   ```
4. Update progress in generation loop:
   ```julia
   if show_gui && gen % 5 == 0  # Update every 5 generations
     set_gtk_property!(label, :label, "Generation: $gen/$generations\nPopulation: $(Nm_curr + Nf_curr)\nMales: $Nm_curr | Females: $Nf_curr")
     # Process GUI events to keep window responsive
     while Gtk.event_pending()
       Gtk.iterate()
     end
   end
   ```
5. Close GUI window after simulation completes

**Fallback:** If Gtk not available, print to console instead

---

### **Part 2: Create Simple Runner File**

**New file:** `run_kbuffer_simple.jl`

**Contents:**
```julia
# Simple Runner for RunModel_KBuffer.jl
# Edit parameters below and run: julia --project=@. run_kbuffer_simple.jl

# ========== EDITABLE PARAMETERS ==========
N = 1000              # Initial population size (males + females = 2*N)
generations = 100     # Number of generations to simulate
replicates = 1        # Number of replicate runs
K = N^2              # Carrying capacity (try: N^2, 5*N, 10*N, etc.)
maintain_sex_ratio = true   # true: 50/50 M/F split at K; false: random sampling
show_gui = false      # true: show GUI progress window; false: console only

# Other parameters (usually keep defaults)
mu = 5.0             # Mean trait value
var = 1.0            # Trait variance
a = 1.0              # Selection parameter
rsc = 0.25           # RSC parameter
tradeoff = true      # Enable tradeoff

# ========================================

# Run simulation
include("RunModel_KBuffer.jl")

using DataFrames, CSV, Dates

println("Starting K-buffer simulation...")
println("  N=$N, generations=$generations, replicates=$replicates")
println("  K=$K, maintain_sex_ratio=$maintain_sex_ratio")
println("  GUI display: $show_gui")

results = runsim_serial(replicates, N, mu, var, a, rsc, tradeoff, generations, -1, K, maintain_sex_ratio, show_gui)
data = DataFrame(results, [:MeanMale,:MeanFemale,:SDMale,:SDFemale,:cor,:MeanCount,:SDCount,:is,:int,:BMale,:GMale,:BFemale,:GFemale,:BSperm,:GSperm,:GMF,:GMS,:GFS,:a,:M
```

