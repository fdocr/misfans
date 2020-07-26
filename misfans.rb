require 'daemons'
require 'rpi_gpio'
require 'logger'

Daemons.run_proc('misfans.rb') do
  logger = Logger.new('/var/log/misfans.log')

  RPi::GPIO.set_numbering :board

  pin_num = 11
  RPi::GPIO.setup pin_num, :as => :output

  module Status
    ON = 0
    OFF = 1
  end

  on_ticks = 0
  off_ticks = 0
  temp = 0
  current_status = Status::OFF

  logger.info { "misfans starting..." }

  begin
    loop do
      measurement = `vcgencmd measure_temp`
      temp = /temp=(?<temp>\d+\.\d+)'C/.match(measurement)[:temp].to_f
      logger.info { "Temp: #{temp} 'C" }

      #  Update statei only if necessary past thresholds
      if current_status == Status::ON && temp < 55  
        RPi::GPIO.set_low pin_num
        current_status  = Status::OFF
        logger.info { "FAN OFF" }
      elsif current_status == Status::OFF && temp > 72
        RPi::GPIO.set_high pin_num
        current_status  = Status::ON
        logger.info { "FAN ON" }
      end

      if current_status == Status::ON
        on_ticks += 1
      else
        off_ticks += 1
      end

      total_ticks = on_ticks + off_ticks
      if (total_ticks % (3 * 15)) == 0
        # Report every 10s * 6 * 15 ticks (15 minutes)
        on_percent = (on_ticks.to_f / total_ticks) * 100
        off_percent = (off_ticks.to_f / total_ticks) *  100
        logger.info { "-"*15  }
        logger.info { "Total ticks: #{total_ticks}" }
        logger.info { "ON: #{on_ticks} (#{on_percent}%)" }
        logger.info {  "OFF: #{off_ticks} (#{off_percent}%)" }
        logger.info { "-"*15  }
      end

      sleep 20
    end
  rescue Exception => e
    logger.info { "Cleaning up..." }
  end

  RPi::GPIO.clean_up
  logger.info { "Bye" }
end

