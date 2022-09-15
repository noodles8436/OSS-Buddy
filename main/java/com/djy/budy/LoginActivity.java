package com.djy.budy;

import static android.speech.tts.TextToSpeech.ERROR;

import android.content.Context;
import android.content.Intent;
import android.location.LocationManager;
import android.os.Bundle;
import android.os.Vibrator;
import android.speech.tts.TextToSpeech;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;

import androidx.appcompat.app.AppCompatActivity;

import java.util.ArrayList;
import java.util.Locale;

//메인 페이지 - 위치 불러오는 부분
public class LoginActivity extends AppCompatActivity {
    private TextToSpeech tts;
    private TextView txtResult;
    static String identify=null;
    String k=null;
    String next_route_nu=null;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main); //xml 연결된 파일
        Button resbutton = (Button) findViewById(R.id.reservation);

        final int[] number_of_clicks = {0};
        final boolean[] thread_started = {false};
        final int DELAY_BETWEEN_CLICKS_IN_MILLISECONDS = 250;

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

        //위치
        final LocationManager lm = (LocationManager) getSystemService(Context.LOCATION_SERVICE);
        //double[] loca = {-2, -2};
        //loca = GPS();
        //txtResult.setText(loca[0] + "\n" + loca[1]);

        resbutton.setOnClickListener(new DoubleClickListener() {
            @Override
            public void onDoubleClick() {
                k = changnum().getRouteNo();
                identify = k;
                resbutton.setText(String.valueOf(k));
                tts.speak(String.valueOf(resbutton.getText()), TextToSpeech.QUEUE_FLUSH,null);

            }

            @Override
            public void onSingleClick() {
                tts.speak(String.valueOf(resbutton.getText()), TextToSpeech.QUEUE_FLUSH,null);

            }
        });

        resbutton.setOnLongClickListener(new View.OnLongClickListener() {
                //길게 클릭할 때
                @Override
                public boolean onLongClick(View view) {
                    if (identify.equals(null)) {
                        tts.speak("버스를 찾으시려면 더블클릭으로 넘겨주세요", TextToSpeech.QUEUE_FLUSH, null);
                    } else {
                        tts.speak(identify + "버스로 예약하시겠습니까?", TextToSpeech.QUEUE_FLUSH, null);
                        Intent intent = new Intent(LoginActivity.this, ReservationActivity.class);
                        startActivity(intent);
                    }
                    return false;
                }
            });


    }

    public BusArrival changnum() {
        int index =0;
        int nextint=0;
        ArrayList<BusArrival> buslist=Network.getBusList();
        if(buslist.size()!=0) {
            if (next_route_nu == null) {
                if (buslist.size() > 1)
                    next_route_nu = buslist.get(1).getRouteNo();
                return buslist.get(0);
            } else {
                if (buslist.size() > 1) {
                    for (int i = 0; i < buslist.size(); i++) {
                        if (next_route_nu.equals(buslist.get(i))) {
                            index = i;
                            break;
                        }
                    }
                    nextint = index + 1;
                    if (nextint > buslist.size())
                        nextint = 0;
                }
                next_route_nu = buslist.get(nextint).getRouteNo();
                return buslist.get(index);
            }
        }
        else
            return null;
    }





}
