require 'daemons'

def custom_show_status(app)
  # Display the default status information
  app.default_show_status

  puts "Log file status:"
  puts `ls -lh /var/log/misfans.log`
end

Daemons.run('misfans.rb', { show_status_callback: :custom_show_status })
