package com.example.realbusdriver;

public class BusReserve {

    private String stationName;
    private int ArrivalLeftNode;

    public BusReserve(String stationName, int ArrivalLeftNode) {
        this.stationName = stationName;
        this.ArrivalLeftNode = ArrivalLeftNode;
    }

    public String getStationName() {
        return this.stationName;
    }

    public int getArrivalLeftNode() {
        return this.ArrivalLeftNode;
    }

}
