launch:
	arm-none-eabi-gcc -c -O0 -mcpu=cortex-m4 -Wall main.c -o main.o
	arm-none-eabi-gcc -c -O0 -mcpu=cortex-m4 -Wall gpio.c -o gpio.o
	arm-none-eabi-gcc -c -O0 -mcpu=cortex-m4 -Wall delay.c -o delay.o
	arm-none-eabi-gcc -x assembler-with-cpp -c -O0 -mcpu=cortex-m4 -mthumb -Wall -fmessage-length=0 core.s -o core.o
	arm-none-eabi-gcc core.o main.o gpio.o delay.o -mcpu=cortex-m4 -mthumb -Wall --specs=nosys.specs -nostdlib -lgcc -T./linka.ld -o main.elf
clean:
	rm *.o
	rm *.elf
open:
	openocd -f /usr/share/openocd/scripts/interface/stlink.cfg -f /usr/share/openocd/scripts/target/stm32f4x.cfg
