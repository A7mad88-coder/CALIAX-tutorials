/*
 * Copyright (c) 2016, Freescale Semiconductor, Inc.
 * Copyright 2016-2017 NXP
 * All rights reserved.
 *
 * SPDX-License-Identifier: BSD-3-Clause

This script generates a unique ID using PUF
 */

#include "board.h"
#include "pin_mux.h"
#include <stdbool.h>
#include "fsl_power.h"
#include "fsl_usart_cmsis.h"
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include "fsl_device_registers.h"
#include "fsl_debug_console.h"
#include "board.h"
#include "fsl_puf.h"
#include "fsl_iap.h"
#include "fsl_iap_ffr.h"
#include "pin_mux.h"
#include "clock_config.h"
#include "fsl_power.h"
#include "fsl_hashcrypt.h"



/*******************************************************************************
 * Definitions
 ******************************************************************************/
#define DEMO_USART Driver_USART0
#define DEMO_USART1 Driver_USART1
#define ECHO_BUFFER_LENGTH 300

#define CORE_CLK_FREQ CLOCK_GetFreq(kCLOCK_CoreSysClk)
/* Worst-case time in ms to fully discharge PUF SRAM */
#define PUF_DISCHARGE_TIME 400
#define PUF_INTRINSIC_KEY_SIZE 16

/*******************************************************************************
 * PUF Variables
 ******************************************************************************/

flash_config_t flashInstance;
#define FLASHSTORE_BASEADR 0x9E600
#define FLASHSTORE_LEN 0x1192


#define TEST_ASSERT(a)       \
    if (!(a))                \
    {                        \
        PRINTF("error\r\n"); \
        do                   \
        {                    \
        } while (1);         \
    }


typedef struct
{
  uint8_t activationCode[PUF_ACTIVATION_CODE_SIZE];
}sPufData;

sPufData pufCmpaData;


/*******************************************************************************
 * Code
 ******************************************************************************/
uint32_t USART0_GetFreq(void)
{
    return CLOCK_GetFlexCommClkFreq(0U);
}
uint32_t USART1_GetFreq(void)
{
    return CLOCK_GetFlexCommClkFreq(1U);
}

/* USART  callback */
void USART_Callback(uint32_t event){}


void PrintMem(uint8_t * adr, uint32_t len, uint32_t seg)
{
	uint32_t i = 0;
	while (i < len)
	{

	  if ((i % seg) == 0)
		PRINTF("\n\r%4d: ",i);

	  PRINTF("%2x ", adr[i++]);
	}
	putchar(0xD); putchar(0xA);
}

void Flash_ReadAC(uint8_t ** acBuf)
{
	*acBuf = &(((sPufData*)FLASHSTORE_BASEADR)->activationCode[0]);
}


uint8_t * StartPuf(void)
{
  status_t status;
  uint8_t *pac;
  while(1)
  {
      Flash_ReadAC(&pac);
      PUF_Deinit(PUF, PUF_DISCHARGE_TIME, CORE_CLK_FREQ);

      /* Reinitialize PUF after enroll */
      status = PUF_Init(PUF, PUF_DISCHARGE_TIME, CORE_CLK_FREQ);
      if (status != kStatus_Success)
      {
          PRINTF("\nError Initializing PUF!\r\n");
          break;
      }

      /* Start PUF by loading generated activation code */
      status = PUF_Start(PUF, pac, sizeof(pufCmpaData.activationCode));
      if (status != kStatus_Success)
      {
          PRINTF("\nError during Start !\r\n");
          break;
      }
      PRINTF("\nThe PUF is started\r\n");
      break;
  }
  return pac;
}


int main(void)
{

	memset(&flashInstance, 0, sizeof(flash_config_t));

	FLASH_Init(&flashInstance);
	FFR_Init(&flashInstance);

	PRINTF("Asvin ID: \n");

    /* set BOD VBAT level to 1.65V */
    POWER_SetBodVbatLevel(kPOWER_BodVbatLevel1650mv, kPOWER_BodHystLevel50mv, false);
    /* attach 12 MHz clock to FLEXCOMM0 (debug console) */

    CLOCK_AttachClk(BOARD_DEBUG_UART_CLK_ATTACH);
   	BOARD_InitPins();
   	BOARD_BootClockFROHF96M();
   	BOARD_InitDebugConsole();
   	USART1_InitPins();

    DEMO_USART1.Initialize(USART_Callback);
	DEMO_USART1.PowerControl(ARM_POWER_FULL);

	/* Set baudrate. */
	DEMO_USART1.Control(ARM_USART_MODE_ASYNCHRONOUS, BOARD_DEBUG_UART_BAUDRATE);

	uint8_t *pkey = 0;
	status_t status;
	size_t outLength;
	char key[1192] = {0};
	char key1[1192] = {0};
	char sha256hashkey[64] = {0};
	int length;
    char output[32];
    char tempbuf[64] = {0};

    pkey = StartPuf();

    PRINTF("Activation Code:");
	PrintMem(pkey, 32, 32);

	for(int i = 0; i < 1192; i++){
		sprintf(key, "%02X", pkey[i]);
		key1[i*2] = key[0];
		key1[i*2+1] = key[1];
	}

	HASHCRYPT_Init(HASHCRYPT);
    length    = sizeof(key1);
    outLength = sizeof(output);
    memset(&output, 0, outLength);

    /************************ SHA-256 **************************/
    status = HASHCRYPT_SHA(HASHCRYPT, kHASHCRYPT_Sha256, key1, length, output, &outLength);
    TEST_ASSERT(kStatus_Success == status);
    TEST_ASSERT(outLength == 32u);


    for(int i = 0; i < 64; i++){
		sprintf(tempbuf, "%02X", output[i]);
		sha256hashkey[i*2] = tempbuf[0];
		sha256hashkey[i*2+1] = tempbuf[1];
   	}
    sha256hashkey[64] = '\0';
	HASHCRYPT_Deinit(HASHCRYPT);

	printf("AsvinID: %s\r\n", sha256hashkey);

	while(1){

	}

}




