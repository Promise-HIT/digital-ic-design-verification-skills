# Run in Vivado batch mode. Preserve the supplied checkpoint.
if {$argc != 2} {
    puts stderr "Usage: -tclargs input.dcp new-report-directory"
    exit 2
}
proc write_reports {checkpoint directory} {
    if {![file isfile $checkpoint]} { error "Missing checkpoint: $checkpoint" }
    if {[file exists $directory]} { error "Report directory already exists: $directory" }
    open_checkpoint $checkpoint
    file mkdir $directory
    puts "Vivado [version -short], clocks: [llength [get_clocks -quiet *]]"
    report_timing_summary -report_unconstrained -file [file join $directory timing.rpt]
    report_utilization -file [file join $directory utilization.rpt]
    close_design
}
if {[catch {write_reports {*}$argv} message]} {
    puts stderr "Checkpoint reports failed: $message"
    exit 1
}
exit 0
