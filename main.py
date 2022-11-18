from machine import ADC, Pin, RTC, lightsleep
import utime
import Pico_ePaper_2_66_B

if __name__=='__main__':
    soil0 = ADC(Pin(26))
    soil1 = ADC(Pin(27))
    min_moisture=0
    max_moisture=65535

    readDelay = 0.5
    
    separator = "-------------------"
    offset = 10

    epd = Pico_ePaper_2_66_B.EPD_2in9_B()
    rtc = RTC()

    while True:
        dt = rtc.datetime()
        ts = "%04d/%02d/%02d %02d:%02d:%02d" % (dt[0:3] + dt[4:7])
        adc0 = soil0.read_u16()
        adc1 = soil1.read_u16()
        moisture0 = (max_moisture-adc0)*100/(max_moisture-min_moisture)
        moisture1 = (max_moisture-adc1)*100/(max_moisture-min_moisture)
        print(ts + ": moisture0: " + "%.2f" % moisture0 +"% (adc: "+ str(adc0) + ")" + " moisture1:" + "%.2f" % moisture1 + "% (adc: " + str(adc1) + ")")
        disp_moisture0 = "%.2f" % moisture0 + "%"
        disp_moisture1 = "%.2f" % moisture1 + "%"
        disp_adc0 = "adc: " + str(adc0)
        disp_adc1 = "adc: " + str(adc1)
        utime.sleep(readDelay)

        epd.Clear(0xff, 0xff)
    
        epd.imageblack.fill(0xff)
        epd.imagered.fill(0xff)
        epd.imageblack.text(ts, 0, offset, 0x00)
        epd.imageblack.text(separator, 0, offset + 15, 0x00)
        epd.imageblack.text("moisture0", 0, offset + 30, 0x00)
        epd.imagered.text(disp_moisture0, 0, offset + 45, 0x00)
        epd.imageblack.text(disp_adc0, 0, offset + 60, 0x00)
        epd.imageblack.text(separator, 0, offset + 75, 0x00)
        epd.imageblack.text("moisture1", 0, offset + 90, 0x00)
        epd.imagered.text(disp_moisture1, 0, offset + 105, 0x00)
        epd.imageblack.text(disp_adc1, 0, offset + 120, 0x00)
        epd.imageblack.text(separator, 0, offset + 135, 0x00)
        epd.display()
        epd.delay_ms(2000)
        
        lightsleep(200000)
        
    
#        break
    
#    epd.Clear(0xff, 0xff)
#    epd.delay_ms(2000)
#    print("sleep")
#    epd.sleep()