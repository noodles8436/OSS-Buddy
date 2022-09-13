package com.djy.budy;

import static android.speech.tts.TextToSpeech.ERROR;
import android.Manifest;
import android.content.Context;
import android.content.pm.PackageManager;
import android.location.Location;
import android.location.LocationManager;
import android.os.Build;
import android.os.Bundle;
import android.os.VibrationEffect;
import android.os.Vibrator;
import android.speech.tts.TextToSpeech;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;
import androidx.annotation.RequiresApi;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.app.ActivityCompat;
import androidx.core.content.ContextCompat;
import com.google.firebase.auth.FirebaseAuth;
import java.util.Locale;

//메인 페이지 - 위치 불러오는 부분
public class LoginActivity extends AppCompatActivity {
    private TextToSpeech tts;
    private TextView txtResult;
    public static FirebaseAuth currentFirebaseUser;
    int busn=0;
    int[] busnum = {22,23,24};
    final int[] identify = {0};
    final int[] k = {0};

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main); //xml 연결된 파일
        txtResult = (TextView) findViewById(R.id.txtResult);
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
        double[] loca = {-2, -2};
        loca = GPS();
        txtResult.setText(loca[0] + "\n" + loca[1]);

        resbutton.setOnClickListener(new DoubleClickListener() {
            @Override
            public void onDoubleClick() {
                k[0] = changnum(busnum);
                identify[0] = k[0];
                resbutton.setText(String.valueOf(k[0]));
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
                if (identify[0]==0) {
                    tts.speak("버스를 찾으시려면 더블클릭으로 넘겨주세요", TextToSpeech.QUEUE_FLUSH, null);
                } else {
                    tts.speak(String.valueOf(identify[0]) + "버스로 예약하시겠습니까?", TextToSpeech.QUEUE_FLUSH, null);

                }
                return false;
            }
        });
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
            ActivityCompat.requestPermissions(LoginActivity.this, new String[]{Manifest.permission.ACCESS_FINE_LOCATION},
                    0);
        } else {
            Location location = lm.getLastKnownLocation(LocationManager.GPS_PROVIDER);
            //loca[0] = location.getLongitude();
            //loca[1] = location.getLatitude();
            Network.setUser_Lati(location.getLatitude());
            Network.setUser_Long(location.getLongitude());
            return loca;
        }return loca;
    }

    public int changnum(int[] bnum) {
        if (busn >= bnum.length - 1) {
            busn = 0;
        } else
            busn++;
        int resultbnum = bnum[busn];

        return resultbnum;
    }

}
