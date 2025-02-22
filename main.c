#include "gpio.h"
#include "delay.h" // Include the delay header

int main() {
    gpio_init(); // Initialize GPIO (enable clock, configure pin as output)

    while (1) {
        gpio_toggle(); // Toggle the LED (set high, then low)
        delay_ms(500); // Delay for 500 milliseconds (adjust as needed)
    }

    return 0; // This is technically never reached in this example, but good practice
}