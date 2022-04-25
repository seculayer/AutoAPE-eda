# syntax=docker/dockerfile:1.3
FROM registry.seculayer.com:31500/ape/python-base:py3.7 as builder
MAINTAINER jinkim "jinkim@seculayer.com"

ARG app="/opt/app"

RUN pip3.7 install wheel && git config --global http.sslVerify false

# pycmmn setup
# specific branch
RUN --mount=type=secret,id=token git clone --depth=5 -c http.extraHeader="Authorization: Bearer $(cat /run/secrets/token)" --single-branch -b SLCAI-54-automl-module https://ssdlc-bitbucket.seculayer.com:8443/scm/slaism/autoape-pycmmn.git $app/pycmmn
#RUN --mount=type=secret,id=token git clone --depth=5 -c http.extraHeader="Authorization: Bearer $(cat /run/secrets/token)" https://ssdlc-bitbucket.seculayer.com:8443/scm/slaism/autoape-pycmmn.git $app/pycmmn
WORKDIR $app/pycmmn
RUN pip3.7 install -r requirements.txt -t $app/pycmmn/lib && python3.7 setup.py bdist_wheel

# eda setup
# specific branch
RUN --mount=type=secret,id=token git clone --depth=5 -c http.extraHeader="Authorization: Bearer $(cat /run/secrets/token)" --single-branch -b SLCAI-54-automl-module https://ssdlc-bitbucket.seculayer.com:8443/scm/slaism/autoape-eda.git $app/eda
#RUN --mount=type=secret,id=token git clone --depth=5 -c http.extraHeader="Authorization: Bearer $(cat /run/secrets/token)" https://ssdlc-bitbucket.seculayer.com:8443/scm/slaism/autoape-eda.git $app/eda

WORKDIR $app/eda
RUN pip3.7 install -r $app/eda/requirements.txt -t $app/eda/lib && python3.7 setup.py bdist_wheel



FROM registry.seculayer.com:31500/ape/python-base:py3.7 as app

ARG app="/opt/app"
ENV LANG=en_US.UTF-8 LANGUAGE=en_US:en LC_ALL=en_US.UTF-8

# pycmmn install
RUN mkdir -p /eyeCloudAI/app/ape/pycmmn
WORKDIR /eyeCloudAI/app/ape/pycmmn

COPY --from=builder "$app/pycmmn/lib" /eyeCloudAI/app/ape/pycmmn/lib
COPY --from=builder "$app/pycmmn/dist/pycmmn-1.0.0-py3-none-any.whl" \
        /eyeCloudAI/app/ape/pycmmn/pycmmn-1.0.0-py3-none-any.whl

RUN pip3.7 install /eyeCloudAI/app/ape/pycmmn/pycmmn-1.0.0-py3-none-any.whl --no-dependencies  \
    -t /eyeCloudAI/app/ape/pycmmn/ \
    && rm /eyeCloudAI/app/ape/pycmmn/pycmmn-1.0.0-py3-none-any.whl

# eda install
RUN mkdir -p /eyeCloudAI/app/ape/eda
WORKDIR /eyeCloudAI/app/ape/eda

COPY ./eda.sh /eyeCloudAI/app/ape/eda
RUN chmod +x /eyeCloudAI/app/ape/eda/eda.sh

COPY --from=builder "$app/eda/lib" /eyeCloudAI/app/ape/eda/lib
COPY --from=builder "$app/eda/dist/eda-1.0.0-py3-none-any.whl" \
        /eyeCloudAI/app/ape/eda/eda-1.0.0-py3-none-any.whl

RUN pip3.7 install /eyeCloudAI/app/ape/eda/eda-1.0.0-py3-none-any.whl --no-dependencies  \
    -t /eyeCloudAI/app/ape/eda/ \
    && rm /eyeCloudAI/app/ape/eda/eda-1.0.0-py3-none-any.whl

RUN groupadd -g 1000 aiuser
RUN useradd -r -u 1000 -g aiuser aiuser
RUN chown -R aiuser:aiuser /eyeCloudAI
USER aiuser

CMD []
