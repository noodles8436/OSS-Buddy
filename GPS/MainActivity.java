package com.example.myapplication;

import android.Manifest;
import android.annotation.SuppressLint;
import android.content.Context;
import android.content.pm.PackageManager;
import android.location.Location;
import android.location.LocationListener;
import android.location.LocationManager;
import android.os.Build;
import android.os.Bundle;
import android.os.VibrationEffect;
import android.os.Vibrator;
import android.speech.tts.TextToSpeech;
import android.support.annotation.RequiresApi;
import android.support.v4.app.ActivityCompat;
import android.support.v4.content.ContextCompat;
import android.support.v7.app.AppCompatActivity;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;
import android.widget.Toast;

import static android.speech.tts.TextToSpeech.ERROR;

import java.io.IOException;
import java.util.Locale;

public class MainActivity extends AppCompatActivity {
    private TextToSpeech tts;
    private TextView txtResult;


    @RequiresApi(api = Build.VERSION_CODES.O)
    @Override
    protected void onCreate(Bundle savedInstanceState) {

        Vibrator vibrator = (Vibrator) getSystemService(Context.VIBRATOR_SERVICE);
        tts = new TextToSpeech(this, new TextToSpeech.OnInitListener() {
            @Override
            public void onInit(int status) {
                if (status != ERROR) {
                    // 언어를 선택한다.
                    tts.setLanguage(Locale.KOREAN);
                }
            }
        });

        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        Button button1 = (Button) findViewById(R.id.button1);
        txtResult = (TextView) findViewById(R.id.txtResult);
        double[] loca = {-2, -2};
        loca = GPS();
        txtResult.setText(loca[0] + "\n" + loca[1]);

    }
    @RequiresApi(api = Build.VERSION_CODES.O)
    public double[] GPS() {
        final LocationManager lm = (LocationManager) getSystemService(Context.LOCATION_SERVICE);
        double[] loca = new double[2];
        double[] failure = {-1, -1};
        if (Build.VERSION.SDK_INT >= 23 &&
                ContextCompat.checkSelfPermission(getApplicationContext(), Manifest.permission.ACCESS_FINE_LOCATION) != PackageManager.PERMISSION_GRANTED) {
            // vibrator.vibrate(500);
            VibrationEffect vibe = VibrationEffect.createOneShot(500, VibrationEffect.DEFAULT_AMPLITUDE);
            //vibrator.vibrate(VibrationEffect.EFFECT_TICK, );
            tts.speak("허용을 눌러 권한 설정을 해주세요.", TextToSpeech.QUEUE_FLUSH, null);
            ActivityCompat.requestPermissions(MainActivity.this, new String[]{Manifest.permission.ACCESS_FINE_LOCATION},
                    0);
        } else {
                Location location = lm.getLastKnownLocation(LocationManager.GPS_PROVIDER);
                loca[0] = location.getLongitude();
                loca[1] = location.getLatitude();
                return loca;
        }return loca;
    }
}