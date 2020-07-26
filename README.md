## misfans

rPi experiment to automate a fan accesory to switch between ON/OFF based on temperature measurements. 

### Requirements

A ruby runtime installed. If new to ruby I recomend [RVM](https://rvm.io/): `curl -sSL https://get.rvm.io | bash -s stable --ruby`

Also install Bundler: `gem install bundler`

### Installing

Clone the repo `git clone https://github.com/fdoxyz/misfans.git` and move into the directory (`cd misfans`).

Logging is done directly to the file `/var/log/misfans.log`. Make sure the user running the deamon has write access to the file, if you need access or you're not sure first do `sudo touch /var/log/misfans.log` and then `chown <YOUR_USER> /var/log/misfans.log`.

Install dependencies `bundle install` and start the daemon with `ruby daemon start`. misfans is using the [Daemons](https://github.com/thuehlinger/daemons) gem, so __from within this directory__ you can use `ruby daemon.rb status`, `ruby daemon.rb restart`, `ruby daemon.rb stop` to interact with the daemon.

Once the daemon is running you should expect the fan to be triggered/enabled by a GPIO pin if the temperature rises above 72 'C and the fans will stop when the temperature falls below 55 'C.

__To-Do (a lot):__
- [ ] Use Daemons' argument feature for data
- [ ] Organize in a proper class & make less of a script
- [ ] Consider embedding in Docker container (ruby runtime dependency)
- [ ] Test

If interested reach out with an issue or drop a PR :)
