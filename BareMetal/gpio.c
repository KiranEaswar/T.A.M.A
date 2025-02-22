#include "gpio.h"

void gpio_init(void) {
    // 1. Enable GPIOC clock  <--- CORRECTED: Using APB1ENR
    RCC_AHB1ENR |= (1 << GPIOC_EN_BIT);

    // 2. Configure PC13 as output
    GPIOC_MODER |= (1 << (LED_PIN * 2));   // Set as output
    GPIOC_MODER &= ~(1 << (LED_PIN * 2 + 1)); // Clear the corresponding bit
}

void gpio_toggle(void) {
    GPIOC_ODR ^= (1 << LED_PIN);  // Toggle the LED pin
}
