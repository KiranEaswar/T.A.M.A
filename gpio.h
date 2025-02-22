#ifndef GPIO_H
#define GPIO_H

#include <stdint.h>

#define GPIOC_BASE          0x40020800UL  // GPIOC base address
#define RCC_AHB1ENR_OFFSET  0x30UL      // Offset of AHB1ENR register in RCC
#define GPIO_MODER_OFFSET   0x00UL       // Offset of MODER register in GPIOC
#define GPIO_ODR_OFFSET     0x14UL       // Offset of ODR register in GPIOC
#define RCC_BASE            0x40023800UL // RCC Base Address
#define GPIOC_EN_BIT        2             // Bit in RCC_AHB1ENR to enable GPIOC clock

// *** LED is connected to PC13 ***
#define LED_PIN             13

// Macros for register access
#define GPIOC_MODER       (*((volatile uint32_t*)(GPIOC_BASE + GPIO_MODER_OFFSET)))
#define GPIOC_ODR         (*((volatile uint32_t*)(GPIOC_BASE + GPIO_ODR_OFFSET)))
#define RCC_AHB1ENR       (*((volatile uint32_t*)(RCC_BASE + RCC_AHB1ENR_OFFSET)))

// Function prototypes
void gpio_init(void);
void gpio_toggle(void);

#endif // GPIO_H