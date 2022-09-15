package com.djy.budy;

import static android.speech.tts.TextToSpeech.ERROR;

import android.Manifest;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.os.Build;
import android.os.Bundle;
import android.os.Handler;
import android.os.VibrationEffect;
import android.speech.tts.TextToSpeech;

import androidx.annotation.RequiresApi;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.app.ActivityCompat;
import androidx.core.content.ContextCompat;

import java.util.Locale;

public class Loading_page extends AppCompatActivity {

    private TextToSpeech tts;
    private static Thread gpsThread = null;
    private static boolean isRunThread = false;
    private GPSTracker gps;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_loading_page);
        tts = new TextToSpeech(this, new TextToSpeech.OnInitListener() {
            @Override
            public void onInit(int status) {
                if (status != ERROR) {
                    // 언어를 선택한다.
                    tts.setLanguage(Locale.KOREAN);
                }
            }
        });
        Handler handler = new Handler();
        handler.postDelayed(new Runnable() {
            public void run() {
                // Intent intent = new Intent(getBaseContext(), User_select.class);
                // startActivity(intent);
                Network.readyforLocation();
                startActivity(new Intent(Loading_page.this, LoginActivity.class));
                finish();
            }
        }, 3000);
        gps = new GPSTracker(Loading_page.this);
        //getLocation();
        startGPS();
    }

    private void startGPS(){
        if(gpsThread == null){
            gpsThread = new Thread(){
                public void run(){
                    isRunThread = true;
                    while(isRunThread){
                        gps.getLocation();
                        Network.setUserLati(gps.getLatitude());
                        Network.setUserLong(gps.getLongitude());
                        try {
                            sleep(1000);
                        } catch (InterruptedException e) {
                            e.printStackTrace();
                        }
                    }
                }
            };
        }
        gpsThread.start();
    }

    private void stopGPS(){
        if(gpsThread != null){
            isRunThread = false;
        }
    }

    @RequiresApi(api = Build.VERSION_CODES.O)
    public double[] GPS() {
        double[] loca = new double[2];
        double[] failure = {-1, -1};
        if (Build.VERSION.SDK_INT >= 23 &&
                ContextCompat.checkSelfPermission(getApplicationContext(), Manifest.permission.ACCESS_FINE_LOCATION) != PackageManager.PERMISSION_GRANTED) {
            VibrationEffect vibe = VibrationEffect.createOneShot(500, VibrationEffect.DEFAULT_AMPLITUDE);
            tts.speak("허용을 눌러 권한 설정을 해주세요.", TextToSpeech.QUEUE_FLUSH, null);
            ActivityCompat.requestPermissions(Loading_page.this, new String[]{Manifest.permission.ACCESS_FINE_LOCATION},
                    0);
        } else {
            //Location location = lm.getLastKnownLocation(LocationManager.NETWORK_PROVIDER);
            //Network.setUserLati(location.getLatitude());
            //Network.setUserLong(location.getLongitude());
            return loca;
        }return loca;
    }
}

