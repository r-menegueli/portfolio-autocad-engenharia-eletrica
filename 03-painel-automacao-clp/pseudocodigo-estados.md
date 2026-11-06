# Pseudocódigo e diagrama de estados

> EXEMPLO CONDICIONAL, NÃO APROVADO: a lógica LSH-inicia / LSL-encerra / LSHH-solicita
> reserva só pode ser considerada após aprovação da filosofia de processo V01. Não
> implementar para enchimento sem revisar as ações dos níveis e identificar cada tanque.

## Estados

```text
DESENERGIZADO -> PRONTO -> BOMBA_1 ou BOMBA_2 -> PRONTO
                       \-> DUAS_BOMBAS -> PRONTO
qualquer estado -> FALHA_TRAVADA -> PRONTO (somente após causa removida + rearme)
```

`MANUAL` é um modo de comando superposto aos estados, sempre subordinado aos mesmos
permissivos físicos e lógicos.

## Pseudocódigo independente de fabricante

```text
permissivo_geral := KSR_OK AND KDRY_OK AND FONTE_24V_OK
apta_1 := permissivo_geral AND RT1_OK AND NOT falha_1
apta_2 := permissivo_geral AND RT2_OK AND NOT falha_2

IF NOT permissivo_geral THEN
    comando_1 := FALSE
    comando_2 := FALSE
    memorizar_falha()
END_IF

IF sensores_incoerentes() THEN
    bloquear_automatico()
    memorizar_alarme_sensor()
END_IF

IF modo_auto AND borda_subida(LSH) AND permissivo_geral THEN
    demanda := TRUE
    titular := titular_proxima
END_IF

IF demanda AND titular = 1 AND apta_1 THEN comando_1 := TRUE END_IF
IF demanda AND titular = 2 AND apta_2 THEN comando_2 := TRUE END_IF

IF falha_partida_1 OR NOT RT1_OK THEN
    comando_1 := FALSE
    falha_1 := TRUE
    IF demanda AND apta_2 THEN comando_2 := TRUE END_IF
END_IF

IF falha_partida_2 OR NOT RT2_OK THEN
    comando_2 := FALSE
    falha_2 := TRUE
    IF demanda AND apta_1 THEN comando_1 := TRUE END_IF
END_IF

IF demanda AND LSHH AND tempo(LSHH) >= 10 s THEN
    IF apta_1 THEN comando_1 := TRUE END_IF
    IF apta_2 THEN comando_2 := TRUE END_IF
END_IF

IF demanda AND LSL THEN
    comando_1 := FALSE
    comando_2 := FALSE
    demanda := FALSE
    titular_proxima := outra_bomba(titular)
END_IF

IF modo_manual THEN
    comando_1 := selo(S2_PARTIR, S3_PARAR) AND apta_1
    comando_2 := selo(S4_PARTIR, S5_PARAR) AND apta_2
END_IF

IF tempo_demanda >= 30 min THEN
    comando_1 := FALSE
    comando_2 := FALSE
    memorizar_alarme_tempo()
END_IF

H5 := qualquer_falha_ativa_ou_memorizada
BZ1 := H5 AND NOT alarme_reconhecido
```

## Observações de implementação

- As entradas devem ser filtradas contra ruído e os sensores submetidos a diagnóstico.
- Memórias retentivas devem possuir valor inicial documentado e estratégia de corrupção.
- Temporizadores e bordas precisam ser implementados com blocos equivalentes da
  plataforma escolhida, seguindo IEC 61131-3.
- A detecção de sensores incoerentes bloqueia nova partida automática, mas a ação para
  bombas já em marcha permanece sem decisão; definir o comportamento de falha antes da
  implementação e do teste de causa e efeito.
- A função de emergência não pode depender deste pseudocódigo.
