local http = require("resty.http")
local cjson = require("cjson")
-- 获取get参数
local params = ngx.req.get_uri_args();
-- TODO: HJD body获取失败
local body_data = ngx.req.read_body();
--创建http客户端实例
local httpc = http.new()
local test_host = os.getenv("TEST_DOMAIN");
local resp, err = httpc:request_uri(test_host,{
    -- method = ngx.req.request_method,
    -- path = ngx.req.http_uri,
    method = "GET",
    path = "/v1/hello",
    headers = {
        ["Host"] = "nginx"
    }
})

if not resp then
    local error_response = {
        ["success"] = 0,
        ["data"] = nil,
        ["errorMsg"] = err
        };
    ngx.say(cjson.encode(error_response));
    return
end

local success_response = {
    status = resp.status,
    success = 1,
    body = body_data,
    params = params,
    data = resp.body
    };
ngx.say(cjson.encode(success_response));

httpc:close()
