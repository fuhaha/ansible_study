def main():
	module = AnsibleModule(
		argument_spec = dict(
			runlevel = dict(default=None, type='str')
		)
	)
	
	# Ansible helps us run commands
	rc, out, err = module.run_command('/sbin/runlevel')
	if rc != 0:
		module.fail_json(msg = "Could not determine current runlevel.",
			rc=rc, err=err)
	
	# Get the runlevel, exit if its not what we expect
	last_runlevel, cur_runlevel = out.split(' ', 1)
	cur_runlevel = cur_runlevel.rstrip()
	if len(cur_runlevel) > 1:
		module.fail_json(msg="Got unexpected output from runlevel.", rc=rc)

	# Do we need to change anything
	if module.params['runlevel'] is None or 
		module.params['runlevel'] == cur_runlevel:
		module.exit_json(changed=False, runlevel=cur_runlevel)
	
	# Check if we are root
	uid = os.geteuid()
	if uid != 0:
		module.fail_json(msg="You need to be root to change the runlevel")
	
	# Attemp to change the runlevel
	rc, out, err = module.run_command('/sbin/init %s' %
 		(module.params['runlevel'])
	
	if rc != 0:
		module.fail_json(msg="Could not change runlevel.", rc=rc, err=err)
	
	# Tell ansible the results
	module.exit_json(changed=True, runlevel=cur_runlevel)

		
		
