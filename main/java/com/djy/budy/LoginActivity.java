package com.djy.budy;
import static android.speech.tts.TextToSpeech.ERROR;

import android.Manifest;
import android.annotation.SuppressLint;
import android.content.Context;
import android.content.pm.PackageManager;
import android.location.Location;
import android.location.LocationListener;
import android.location.LocationManager;
import android.os.Build;
import android.os.Bundle;
import android.os.Vibrator;
import android.speech.tts.TextToSpeech;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;

import androidx.appcompat.app.AppCompatActivity;
import androidx.core.app.ActivityCompat;
import androidx.core.content.ContextCompat;

import java.util.Locale;

public class LoginActivity extends AppCompatActivity {
    private TextToSpeech tts;
    private TextView txtResult;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        //따로 빼서 쓸 버스 예약 버튼
        Button resbutton = (Button) findViewById(R.id.reservation);

        Vibrator vibrator = (Vibrator) getSystemService(Context.VIBRATOR_SERVICE);
        tts = new TextToSpeech(this, new TextToSpeech.OnInitListener() {
            @Override
            public void onInit(int status) {
                if(status != ERROR) {
                    // 언어를 선택한다.
                    tts.setLanguage(Locale.KOREAN);
                }
            }
        });
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        Button button1 = (Button) findViewById(R.id.button1);
        txtResult = (TextView) findViewById(R.id.txtResult);

        final LocationManager lm = (LocationManager) getSystemService(Context.LOCATION_SERVICE);
       /*
        resbutton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                if (Build.VERSION.SDK_INT >= 23 &&
                        ContextCompat.checkSelfPermission(getApplicationContext(), Manifest.permission.RECORD_AUDIO) != PackageManager.PERMISSION_GRANTED) {
                    vibrator.vibrate(500);
                    tts.speak("허용을 눌러 권한 설정을 해주세요.",TextToSpeech.QUEUE_FLUSH,null);
                    ActivityCompat.requestPermissions(MainActivity.this, new String[]{Manifest.permission.RECORD_AUDIO},
                            0);
                }
            }
        });

        */
        button1.setOnClickListener(new View.OnClickListener() {
            @SuppressLint({"MissingPermission", "SetTextI18n"})
            @Override
            public void onClick(View v) {
                if (Build.VERSION.SDK_INT >= 23 &&
                        ContextCompat.checkSelfPermission(getApplicationContext(), Manifest.permission.ACCESS_FINE_LOCATION) != PackageManager.PERMISSION_GRANTED) {
                    vibrator.vibrate(500);
                    tts.speak("허용을 눌러 권한 설정을 해주세요.",TextToSpeech.QUEUE_FLUSH,null);
                    ActivityCompat.requestPermissions(LoginActivity.this, new String[]{Manifest.permission.ACCESS_FINE_LOCATION},
                            0);
                } else {
                    Location location = lm.getLastKnownLocation(LocationManager.GPS_PROVIDER);

                    double longitude = location.getLongitude();
                    double latitude = location.getLatitude();


                    txtResult.setText(
                            "경도 : " + longitude + "\n" +
                                    "위도 : " + latitude + "\n"
                    );


                }
            }
        });

    }

    final LocationListener gpsLocationListener = new LocationListener() {
        public void onLocationChanged(Location location) {

            double longitude = location.getLongitude();
            double latitude = location.getLatitude();

            txtResult.setText(
                    "경도 : " + longitude + "\n" +
                            "위도 : " + latitude + "\n");

        }
    };
}
