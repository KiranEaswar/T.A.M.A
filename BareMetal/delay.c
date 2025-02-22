#include "delay.h"

#define SYSTEM_CORE_CLOCK 84000000 // Example: 84 MHz.  

void delay_ms(uint32_t ms) {
    volatile uint32_t i;
    for (uint32_t j = 0; j < ms; j++) {
        for (i = 0; i < SYSTEM_CORE_CLOCK / 84000; i++) {
            __asm__ volatile (""); 
        }
    }
}
