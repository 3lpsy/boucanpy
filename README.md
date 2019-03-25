# Bounty DNS: A DNS Catcher

Status: Non-functional / WIP

This project is an attempt to implement a lightweight burp collaborator-esc application and consists of two main components: a DNS Server (Custom Python Implemention with dnslib) and an API.

When answering queries, the DNS server hits the API with information regarding the DNS query. The API will then serve the log of the DNS queries via a RESTful HTTP API as well as front-end (HTML/JS) web GUI.

TODO:
- [x] Build DNS Implementation
- [x] Build CLI Foundation
- [ ] Build API Auth Routes
- [ ] Build API Authentication Controls
- [ ] Build API Token Capabilities (Extended Auth Tokens)
- [ ] Build API Zone / DNS Routes
- [ ] Integrate API Callbacks into DNS Server
- [ ] Build ability for webhook's / events 
