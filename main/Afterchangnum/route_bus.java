package com.example.ynbutton;

import java.io.Serializable;

public class route_bus implements Serializable {
    String route;
    public  route_bus(){
        
    }
    public  route_bus(String route){
        this.route=route;
    }
    public String getRoute(){
        return route;
    }
    public void setRoute(String reroute){
        route=reroute;
    }
}
