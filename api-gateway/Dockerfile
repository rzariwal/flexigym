#Download base image ubuntu
FROM ubuntu:18.04
# LABEL about the custom image
LABEL maintainer="rzariwal@gmail.com"
LABEL version="0.1"
LABEL description="This openresty Image with modsec."

ENV PATH="${PATH}:/usr/local/openresty/bin:/usr/local/openresty/luajit/bin"
COPY ssl /usr/local/openresty/nginx/ssl

COPY nginx.conf /usr/local/openresty/nginx/conf/nginx.conf

# Update Ubuntu Software repository
RUN apt-get update
# Install from ubuntu repository
RUN apt install -y git wget openssl g++ flex bison curl doxygen libyajl-dev libgeoip-dev libtool dh-autoreconf libcurl4-gnutls-dev libxml2 libpcre++-dev libxml2-dev && \
    apt install -y apache2-dev autoconf automake build-essential bzip2 checkinstall devscripts flex g++ gcc git graphicsmagick-imagemagick-compat graphicsmagick-libmagick-dev-compat libaio-dev libaio1 libass-dev libatomic-ops-dev libavcodec-dev libavdevice-dev libavfilter-dev libavformat-dev libavutil-dev libbz2-dev libcurl4-openssl-dev libfaac-dev libfreetype6-dev libgd-dev libgeoip-dev libgeoip1 libgif-dev libgpac-dev libgsm1-dev libjack-jackd2-dev libjpeg-dev libjpeg-progs libjpeg8-dev liblmdb-dev libmp3lame-dev libncurses5-dev libopencore-amrnb-dev libopencore-amrwb-dev libpam0g-dev libpcre3 libpcre3-dev libperl-dev libreadline-dev librtmp-dev libsdl1.2-dev libssl-dev libssl1.0.0 libswscale-dev libtheora-dev libtiff5-dev libtool libva-dev libvdpau-dev libvorbis-dev libxml2-dev libxslt-dev libxslt1-dev libxslt1.1 libxvidcore-dev libxvidcore4 libyajl-dev make openssl perl pkg-config tar texi2html unzip zip zlib1g-dev && \
    apt clean && \
    mkdir -p /home/rzariwal && \
    cd /home/rzariwal && \
    git clone https://github.com/SpiderLabs/ModSecurity && \
    cd ModSecurity/ && \
    git checkout v3/master && \
    ./build.sh && \
    git submodule init && \
    git submodule update && \
    ./configure && \
    make && \
    make install && \
    cd .. && \
    wget https://openresty.org/download/openresty-1.15.8.2.tar.gz  && \
    git clone --depth 1 https://github.com/SpiderLabs/ModSecurity-nginx.git && \
    tar xvf openresty-1.15.8.2.tar.gz && \
    ls && \
    cd openresty-1.15.8.2 && \
    ./configure --with-compat --add-dynamic-module=/home/rzariwal/ModSecurity-nginx/ && \
    ln -s /usr/bin/make /usr/bin/gmake && \
    gmake && \
    gmake install && \
    ln -s /usr/local/openresty/bin/openresty /usr/bin/openresty && \
    cd /usr/local/openresty/nginx && \
    mkdir modsec && \
    wget https://raw.githubusercontent.com/SpiderLabs/ModSecurity/v3/master/modsecurity.conf-recommended && \
    mv modsecurity.conf-recommended modsec/modsecurity.conf && \
    cp /home/rzariwal/ModSecurity/unicode.mapping /usr/local/openresty/nginx/modsec && \
    sed -i '1iload_module /usr/local/openresty/nginx/modules/ngx_http_modsecurity_module.so;' /usr/local/openresty/nginx/conf/nginx.conf && \
    sed -i '25imodsecurity on;' /usr/local/openresty/nginx/conf/nginx.conf && \
    sed -i '26imodsecurity_rules_file /usr/local/openresty/nginx/modsec/main.conf;' /usr/local/openresty/nginx/conf/nginx.conf && \
    touch /usr/local/openresty/nginx/modsec/main.conf && \
    echo "Include /usr/local/openresty/nginx/modsec/modsecurity.conf" >> /usr/local/openresty/nginx/modsec/main.conf && \
    echo "Include /usr/local/openresty/nginx/owasp-modsecurity-crs-3.0.2/crs-setup.conf" >> /usr/local/openresty/nginx/modsec/main.conf && \
    echo "Include /usr/local/openresty/nginx/owasp-modsecurity-crs-3.0.2/rules/*.conf" >> /usr/local/openresty/nginx/modsec/main.conf && \
    sed -i '263iSecDebugLog /usr/local/openresty/nginx/logs/debug.log' /usr/local/openresty/nginx/modsec/modsecurity.conf && \
    sed -i '264iSecDebugLogLevel 3' /usr/local/openresty/nginx/modsec/modsecurity.conf && \
    sed -i -e 's/SecAuditEngine RelevantOnly/SecAuditEngine On/g' /usr/local/openresty/nginx/modsec/modsecurity.conf && \
    /usr/local/openresty/bin/opm install bungle/lua-resty-session && \
#    /usr/local/openresty/bin/opm install pintsized/lua-resty-http && \
    /usr/local/openresty/bin/opm install zmartzone/lua-resty-openidc && \
    wget https://github.com/SpiderLabs/owasp-modsecurity-crs/archive/v3.0.2.tar.gz && \
    tar -xvzf v3.0.2.tar.gz && \
    cd owasp-modsecurity-crs-3.0.2 && \
    cp crs-setup.conf.example crs-setup.conf && \
    openresty -t

EXPOSE 443
CMD ["/usr/local/openresty/bin/openresty", "-g", "daemon off;"]
STOPSIGNAL SIGTERM