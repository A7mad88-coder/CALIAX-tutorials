################################################################################
# Automatically-generated file. Do not edit!
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
C_SRCS += \
../drivers/fsl_clock.c \
../drivers/fsl_common.c \
../drivers/fsl_dma.c \
../drivers/fsl_flexcomm.c \
../drivers/fsl_gpio.c \
../drivers/fsl_hashcrypt.c \
../drivers/fsl_iap.c \
../drivers/fsl_inputmux.c \
../drivers/fsl_power.c \
../drivers/fsl_puf.c \
../drivers/fsl_reset.c \
../drivers/fsl_usart.c \
../drivers/fsl_usart_cmsis.c \
../drivers/fsl_usart_dma.c 

OBJS += \
./drivers/fsl_clock.o \
./drivers/fsl_common.o \
./drivers/fsl_dma.o \
./drivers/fsl_flexcomm.o \
./drivers/fsl_gpio.o \
./drivers/fsl_hashcrypt.o \
./drivers/fsl_iap.o \
./drivers/fsl_inputmux.o \
./drivers/fsl_power.o \
./drivers/fsl_puf.o \
./drivers/fsl_reset.o \
./drivers/fsl_usart.o \
./drivers/fsl_usart_cmsis.o \
./drivers/fsl_usart_dma.o 

C_DEPS += \
./drivers/fsl_clock.d \
./drivers/fsl_common.d \
./drivers/fsl_dma.d \
./drivers/fsl_flexcomm.d \
./drivers/fsl_gpio.d \
./drivers/fsl_hashcrypt.d \
./drivers/fsl_iap.d \
./drivers/fsl_inputmux.d \
./drivers/fsl_power.d \
./drivers/fsl_puf.d \
./drivers/fsl_reset.d \
./drivers/fsl_usart.d \
./drivers/fsl_usart_cmsis.d \
./drivers/fsl_usart_dma.d 


# Each subdirectory must supply rules for building sources it contributes
drivers/%.o: ../drivers/%.c
	@echo 'Building file: $<'
	@echo 'Invoking: MCU C Compiler'
	arm-none-eabi-gcc -std=gnu99 -D__REDLIB__ -DCPU_LPC55S69JBD100 -DCPU_LPC55S69JBD100_cm33 -DCPU_LPC55S69JBD100_cm33_core0 -DSERIAL_PORT_TYPE_UART=1 -DSDK_DEBUGCONSOLE=0 -DCR_INTEGER_PRINTF -DPRINTF_FLOAT_ENABLE=0 -D__MCUXPRESSO -D__USE_CMSIS -DDEBUG -DFSL_RTOS_BM -DSDK_OS_BAREMETAL -I"C:\Users\omkar\Documents\MCUXpressoIDE_11.2.1_4149\workspace\asvinid-esp-at\AsvinIDGeneator\drivers" -I"C:\Users\omkar\Documents\MCUXpressoIDE_11.2.1_4149\workspace\asvinid-esp-at\AsvinIDGeneator\component\serial_manager" -I"C:\Users\omkar\Documents\MCUXpressoIDE_11.2.1_4149\workspace\asvinid-esp-at\AsvinIDGeneator\CMSIS" -I"C:\Users\omkar\Documents\MCUXpressoIDE_11.2.1_4149\workspace\asvinid-esp-at\AsvinIDGeneator\CMSIS_driver" -I"C:\Users\omkar\Documents\MCUXpressoIDE_11.2.1_4149\workspace\asvinid-esp-at\AsvinIDGeneator\device" -I"C:\Users\omkar\Documents\MCUXpressoIDE_11.2.1_4149\workspace\asvinid-esp-at\AsvinIDGeneator\board" -I"C:\Users\omkar\Documents\MCUXpressoIDE_11.2.1_4149\workspace\asvinid-esp-at\AsvinIDGeneator\utilities" -I"C:\Users\omkar\Documents\MCUXpressoIDE_11.2.1_4149\workspace\asvinid-esp-at\AsvinIDGeneator\component\lists" -I"C:\Users\omkar\Documents\MCUXpressoIDE_11.2.1_4149\workspace\asvinid-esp-at\AsvinIDGeneator\component\uart" -I"C:\Users\omkar\Documents\MCUXpressoIDE_11.2.1_4149\workspace\asvinid-esp-at\AsvinIDGeneator\board" -I"C:\Users\omkar\Documents\MCUXpressoIDE_11.2.1_4149\workspace\asvinid-esp-at\AsvinIDGeneator\source" -I"C:\Users\omkar\Documents\MCUXpressoIDE_11.2.1_4149\workspace\asvinid-esp-at\AsvinIDGeneator" -I"C:\Users\omkar\Documents\MCUXpressoIDE_11.2.1_4149\workspace\asvinid-esp-at\AsvinIDGeneator\drivers" -I"C:\Users\omkar\Documents\MCUXpressoIDE_11.2.1_4149\workspace\asvinid-esp-at\AsvinIDGeneator\device" -I"C:\Users\omkar\Documents\MCUXpressoIDE_11.2.1_4149\workspace\asvinid-esp-at\AsvinIDGeneator\CMSIS" -I"C:\Users\omkar\Documents\MCUXpressoIDE_11.2.1_4149\workspace\asvinid-esp-at\AsvinIDGeneator\CMSIS_driver" -I"C:\Users\omkar\Documents\MCUXpressoIDE_11.2.1_4149\workspace\asvinid-esp-at\AsvinIDGeneator\startup" -I"C:\Users\omkar\Documents\MCUXpressoIDE_11.2.1_4149\workspace\asvinid-esp-at\AsvinIDGeneator\utilities" -I"C:\Users\omkar\Documents\MCUXpressoIDE_11.2.1_4149\workspace\asvinid-esp-at\AsvinIDGeneator\component\serial_manager" -I"C:\Users\omkar\Documents\MCUXpressoIDE_11.2.1_4149\workspace\asvinid-esp-at\AsvinIDGeneator\component\lists" -I"C:\Users\omkar\Documents\MCUXpressoIDE_11.2.1_4149\workspace\asvinid-esp-at\AsvinIDGeneator\component\uart" -O0 -fno-common -g3 -Wall -mcpu=cortex-m33  -c  -ffunction-sections  -fdata-sections  -ffreestanding  -fno-builtin -fmerge-constants -fmacro-prefix-map="../$(@D)/"=. -mcpu=cortex-m33 -mfpu=fpv5-sp-d16 -mfloat-abi=hard -mthumb -D__REDLIB__ -fstack-usage -specs=redlib.specs -MMD -MP -MF"$(@:%.o=%.d)" -MT"$(@:%.o=%.o)" -MT"$(@:%.o=%.d)" -o "$@" "$<"
	@echo 'Finished building: $<'
	@echo ' '


