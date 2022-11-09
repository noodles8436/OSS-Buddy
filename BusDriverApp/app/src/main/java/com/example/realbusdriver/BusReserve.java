package com.example.realbusdriver;

public class BusReserve {

    private String stationName;
    private int ArrivalLeftNode;
    private boolean isAlarm;

    public BusReserve(String stationName, int ArrivalLeftNode, String isAlarm) {
        this.stationName = stationName;
        this.ArrivalLeftNode = ArrivalLeftNode;
        if(isAlarm.equals("1")){
            this.isAlarm = true;
        }else{
            this.isAlarm = false;   
        }
    }

    public String getStationName() {
        return this.stationName;
    }

    public int getArrivalLeftNode() {
        return this.ArrivalLeftNode;
    }
    
    public boolean getAlarming(){
        return this.isAlarm   
    }

}
