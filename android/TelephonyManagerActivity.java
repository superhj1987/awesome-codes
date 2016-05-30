/**
TelephonyManager类主要提供了一系列用于访问与手机通讯相关的状态和信息的get方法。
其中包括手机SIM的状态和信息、电信网络的状态及手机用户的信息。在应用程序中可以使用这些get方法获取相关数据。
TelephonyManager类的对象可以通过Context.getSystemService(Context.TELEPHONY_SERVICE)方法来获得，
需要注意的是有些通讯信息的获取对应用程序的权限有一定的限制，在开发的时候需要为其添加相应的权限。
**/

package com.ljq.activity;

import java.util.List;

import Android.app.Activity;
import Android.content.Context;
import Android.os.Bundle;
import Android.telephony.CellLocation;
import Android.telephony.NeighboringCellInfo;
import Android.telephony.TelephonyManager;

public class TelephonyManagerActivity extends Activity {

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.main);

        TelephonyManager tm = (TelephonyManager) getSystemService(Context.TELEPHONY_SERVICE);
        /**
         * 返回电话状态
         *
         * CALL_STATE_IDLE 无任何状态时
         * CALL_STATE_OFFHOOK 接起电话时
         * CALL_STATE_RINGING 电话进来时
         */
        tm.getCallState();
        //返回当前移动终端的位置
        CellLocation location=tm.getCellLocation();
        //请求位置更新，如果更新将产生广播，接收对象为注册LISTEN_CELL_LOCATION的对象，需要的permission名称为ACCESS_COARSE_LOCATION。
        location.requestLocationUpdate();
        /**
         * 获取数据活动状态
         *
         * DATA_ACTIVITY_IN 数据连接状态：活动，正在接受数据
         * DATA_ACTIVITY_OUT 数据连接状态：活动，正在发送数据
         * DATA_ACTIVITY_INOUT 数据连接状态：活动，正在接受和发送数据
         * DATA_ACTIVITY_NONE 数据连接状态：活动，但无数据发送和接受
         */
        tm.getDataActivity();
        /**
         * 获取数据连接状态
         *
         * DATA_CONNECTED 数据连接状态：已连接
         * DATA_CONNECTING 数据连接状态：正在连接
         * DATA_DISCONNECTED 数据连接状态：断开
         * DATA_SUSPENDED 数据连接状态：暂停
         */
        tm.getDataState();
        /**
         * 返回当前移动终端的唯一标识
         *
         * 如果是GSM网络，返回IMEI；如果是CDMA网络，返回MEID
         */
        tm.getDeviceId();
        //返回移动终端的软件版本，例如：GSM手机的IMEI/SV码。
        tm.getDeviceSoftwareVersion();
        //返回手机号码，对于GSM网络来说即MSISDN
        tm.getLine1Number();
        //返回当前移动终端附近移动终端的信息
        List<NeighboringCellInfo> infos=tm.getNeighboringCellInfo();
 for(NeighboringCellInfo info:infos){
            //获取邻居小区号
            int cid=info.getCid();
            //获取邻居小区LAC，LAC: 位置区域码。为了确定移动台的位置，每个GSM/PLMN的覆盖区都被划分成许多位置区，LAC则用于标识不同的位置区。
            info.getLac();
            info.getNetworkType();
            info.getPsc();
            //获取邻居小区信号强度
            info.getRssi();
        }
        //返回ISO标准的国家码，即国际长途区号
        tm.getNetworkCountryIso();
        //返回MCC+MNC代码 (SIM卡运营商国家代码和运营商网络代码)(IMSI)
        tm.getNetworkOperator();
        //返回移动网络运营商的名字(SPN)
        tm.getNetworkOperatorName();
        /**
         * 获取网络类型
         *
         * NETWORK_TYPE_CDMA 网络类型为CDMA
         * NETWORK_TYPE_EDGE 网络类型为EDGE
         * NETWORK_TYPE_EVDO_0 网络类型为EVDO0
         * NETWORK_TYPE_EVDO_A 网络类型为EVDOA
         * NETWORK_TYPE_GPRS 网络类型为GPRS
         * NETWORK_TYPE_HSDPA 网络类型为HSDPA
         * NETWORK_TYPE_HSPA 网络类型为HSPA
         * NETWORK_TYPE_HSUPA 网络类型为HSUPA
         * NETWORK_TYPE_UMTS 网络类型为UMTS
         *
         * 在中国，联通的3G为UMTS或HSDPA，移动和联通的2G为GPRS或EGDE，电信的2G为CDMA，电信的3G为EVDO
         */
        tm.getNetworkType();
        /**
         * 返回移动终端的类型
         *
         * PHONE_TYPE_CDMA 手机制式为CDMA，电信
         * PHONE_TYPE_GSM 手机制式为GSM，移动和联通
         * PHONE_TYPE_NONE 手机制式未知
         */
        tm.getPhoneType();
        //返回SIM卡提供商的国家代码
        tm.getSimCountryIso();
        //返回MCC+MNC代码 (SIM卡运营商国家代码和运营商网络代码)(IMSI)
        tm.getSimOperator();
        tm.getSimOperatorName();
        //返回SIM卡的序列号(IMEI)
        tm.getSimSerialNumber();
        /**
         * 返回移动终端
         *
         * SIM_STATE_ABSENT SIM卡未找到
         * SIM_STATE_NETWORK_LOCKED SIM卡网络被锁定，需要Network PIN解锁
         * SIM_STATE_PIN_REQUIRED SIM卡PIN被锁定，需要User PIN解锁
         * SIM_STATE_PUK_REQUIRED SIM卡PUK被锁定，需要User PUK解锁
         * SIM_STATE_READY SIM卡可用
         * SIM_STATE_UNKNOWN SIM卡未知
*/
        tm.getSimState();
        //返回用户唯一标识，比如GSM网络的IMSI编号
        tm.getSubscriberId();
        //获取语音信箱号码关联的字母标识。
        tm.getVoiceMailAlphaTag();
        //返回语音邮件号码
        tm.getVoiceMailNumber();
        tm.hasIccCard();
        //返回手机是否处于漫游状态
        tm.isNetworkRoaming();
        // tm.listen(PhoneStateListener listener, int events) ;

        //解释：
        //IMSI是国际移动用户识别码的简称(International Mobile Subscriber Identity)
        //IMSI共有15位，其结构如下：
        //MCC+MNC+MIN
        //MCC：Mobile Country Code，移动国家码，共3位，中国为460;
        //MNC:Mobile NetworkCode，移动网络码，共2位
        //在中国，移动的代码为电00和02，联通的代码为01，电信的代码为03
        //合起来就是（也是Android手机中APN配置文件中的代码）：
        //中国移动：46000 46002
        //中国联通：46001
        //中国电信：46003
        //举例，一个典型的IMSI号码为460030912121001

        //IMEI是International Mobile Equipment Identity （国际移动设备标识）的简称
        //IMEI由15位数字组成的”电子串号”，它与每台手机一一对应，而且该码是全世界唯一的
        //其组成为：
        //1. 前6位数(TAC)是”型号核准号码”，一般代表机型
        //2. 接着的2位数(FAC)是”最后装配号”，一般代表产地
        //3. 之后的6位数(SNR)是”串号”，一般代表生产顺序号
        //4. 最后1位数(SP)通常是”0″，为检验码，目前暂备用
    }
}
