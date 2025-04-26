
@load base/protocols/conn
@load base/protocols/ssl
@load base/protocols/http
@load base/files/x509
@load policy/tuning/json-logs

event zeek_init() {
    Log::disable_stream(Files::LOG);
    Log::disable_stream(OCSP::LOG);
}
