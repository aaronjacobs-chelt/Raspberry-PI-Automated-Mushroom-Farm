# GPIO Pin Connection Diagram

This diagram shows the connections between the Raspberry Pi GPIO pins and the Energenie ENER002-2PI smart plug controller.

```
                     RASPBERRY PI (Top View)
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│ ┌───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┐   │
│ │ 1 │ 3 │ 5 │ 7 │ 9 │11*│13*│15*│17 │19 │21 │23 │25 │27 │   │
│ ├───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┤   │
│ │ 2 │ 4 │ 6 │ 8 │10 │12 │14 │16*│18*│20 │22*│24 │26 │28 │   │
│ └───┴───┴───┴───┴───┴───┴───┴───┴───┴───┴───┴───┴───┴───┘   │
│                                                             │
│  * = Pins used for Energenie connections                    │
│                                                             │
└─────────────────────────────────────────────────────────────┘
          │   │   │   │   │   │
          │   │   │   │   │   │
          │   │   │   │   │   │
          │   │   │   │   │   │
          │   │   │   │   │   │
          │   │   │   │   │   │
       RED│BLK│WHT│GRN│YEL│BLU│
     ┌────┴───┴───┴───┴───┴───┴────┐
     │                             │
     │    ENERGENIE CONTROLLER     │
     │                             │
     └─────────────┬───────────────┘
                   │
                   │
            ┌──────▼──────┐
            │              │
            │  HUMIDIFIER  │
            │              │
            └──────────────┘
```

## Pin Connection Table

| GPIO Pin | Physical Pin | Wire Color | Function | Description |
|----------|--------------|------------|----------|-------------|
| GPIO17   | Pin 11       | RED        | CTRL1    | Control line 1 |
| GND      | Pin 13       | BLACK      | OUTLET   | Ground connection |
| GPIO27   | Pin 15       | WHITE      | CTRL2    | Control line 2 |
| GPIO22   | Pin 16       | GREEN      | CTRL3    | Control line 3 |
| GPIO23   | Pin 18       | YELLOW     | CTRL4    | Control line 4 |
| GPIO24   | Pin 22       | BLUE       | TRIGGER  | Trigger signal |

## Connection Instructions

1. **Power off your Raspberry Pi** before making any connections
2. Connect each wire from the Energenie controller to the corresponding GPIO pin on the Raspberry Pi
3. Ensure all connections are secure and properly insulated
4. Connect the humidifier to the Energenie smart plug
5. Boot the Raspberry Pi and run the automation script

## Signal Flow Diagram

```
┌─────────────────┐     ┌───────────────────┐     ┌─────────────┐
│                 │     │                   │     │             │
│   Raspberry Pi  │---->│ Energenie Control │---->│ Smart Plug  │
│   GPIO Output   │     │ Signals           │     │ Activation  │
│                 │     │                   │     │             │
└─────────────────┘     └───────────────────┘     └─────────────┘
       │                                                 │
       │                                                 │
       │                                                 v
       │                                          ┌─────────────┐
       │                                          │             │
       │                                          │ Humidifier  │
       v                                          │ Power       │
┌─────────────────┐                              └─────────────┘
│                 │
│  Python Script  │
│  Logic          │
│                 │
└─────────────────┘
```

## Important Notes

- Always double-check connections before powering on your Raspberry Pi
- The script must run with sudo privileges to access GPIO pins
- Test the connections with a multimeter if possible before connecting the humidifier
- The Energenie controller uses a specific control sequence sent through these pins to activate the correct outlet
- If you need to extend any wires, ensure you use appropriate gauge wire and proper insulation

