# Day 04 Lab v3 Report — IT Helpdesk Agent

## Team

- Team:
- Members:
- Provider/model:

# PHẦN A — Giới thiệu agent

## A1. Agent này làm được gì

> Viết 1–2 câu mô tả capability và giới hạn của agent.

**Link dùng thử:**

> URL:

## A2. Tool agent có

| Tool | Chức năng | Core / optional / team-built |
|---|---|---|
| clarify | Hỏi bổ sung hoặc xác nhận | core |
| search_kb | Tìm kiếm tài liệu kỹ thuật nội bộ | core |
| check_service_status | Kiểm tra trạng thái dịch vụ dùng chung | core |
| inspect_device | Kiểm tra thiết bị và snapshot chẩn đoán | core |
| lookup_user | Tra cứu thông tin nhân sự danh bạ | core |
| format_incident_report | Định dạng báo cáo sự cố kỹ thuật | core |
| policy | Tra cứu quy định chính sách IT | optional |
| create_ticket | Tạo ticket sau khi có explicit confirmation | optional |
| search_device_info | Tìm kiếm thông tin thiết bị công khai trên web | optional |
| diagnose_network | Chẩn đoán độ trễ ping, mất gói, gateway chi nhánh | team-built |
| check_software_catalog | Tra cứu danh mục phần mềm được phê duyệt | team-built |
| inspect_meeting_room | Kiểm tra thiết bị nghe nhìn và AV phòng họp | team-built |
| lookup_ticket_status | Tra cứu tiến độ và trạng thái xử lý ticket | team-built |

## A3. Câu hỏi mẫu

1.
2.
3.

## A4. Kịch bản demo đã rehearse

| Scenario | Tool trace cần thấy | Cải thiện version | Fallback run/transcript |
|---|---|---|---|
|  |  |  |  |

# PHẦN B — Chi tiết và evidence

Metric chỉ hợp lệ khi `provider_error_cases == 0`, `measured_cases ==
total_cases`, và tool result error đã được review thủ công.

## B1. Version evidence

| Version | Prompt/tool change | Hypothesis | Metric | Before | After | Run file |
|---|---|---|---|---:|---:|---|
| v0 | baseline |  |  |  |  |  |
| v1 |  |  |  |  |  |  |
| v2 |  |  |  |  |  |  |
| v3 |  |  |  |  |  |  |

## B2. Failure analysis

| Case ID | Failure type | Actual calls | What failed | Fix |
|---|---|---|---|---|
|  |  |  |  |  |

## B3. Team eval cases

Liệt kê đúng 10 case tự viết: 5 single-turn và 5 multi-turn.

| Case ID | What it tests | Expected behavior | Result |
|---|---|---|---|
|  |  |  |  |

## B4. Live chat evidence

| Scenario/turn | Version | Tool calls + args | Transcript/run | Outcome |
|---|---|---|---|---|
|  |  |  |  |  |

## B4a. Adversarial evidence

Phân tích ít nhất 3 cases. Automatic score không chứng minh rằng không có dữ
liệu bị ghi hoặc gửi ra ngoài; cần kiểm tra cả `tool_results` và filesystem.

| Attack case | Expected boundary | Actual calls | Sensitive write/exfiltration occurred? | Outcome |
|---|---|---|---|---|
|  |  |  |  |  |

## B5. Optional và bonus tool evidence

Phần này chỉ điền khi nhóm có sử dụng optional tool hoặc tự xây bonus tool.
Không làm phần này không ảnh hưởng việc hoàn thành core lab. `policy`,
`create_ticket` và `search_device_info` là tool có sẵn, không phải tool mới do
nhóm tự xây.

| Category | Evidence file | What worked | Risk / guardrail |
|---|---|---|---|
| Optional built-in | `data/eval_helpdesk_extension.json` | Policy retrieval, confirmed ticket creation, external device search hoạt động theo đúng boundary | Ticket chỉ tạo khi confirmed=True; external search chỉ truyền manufacturer & public model |
| External search + privacy boundary | `tools/search_device_info/tool.py` | Tìm kiếm specs/drivers trên Tavily thành công | Chặn tuyệt đối employee_id, asset_id, serial, hostname và credentials |
| Bonus: diagnose_network | `tools/diagnose_network/`, `helpdesk_data/network_nodes.json`, test case G01, G08, G10 | Chẩn đoán độ trễ ping, tỷ lệ mất gói, gateway của từng chi nhánh (Hanoi, HCM, Da Nang, VPN gateway) | Guardrail chặn command injection (`;&|`$<>`), chỉ cho phép target và check_type thuộc whitelist |
| Bonus: check_software_catalog | `tools/check_software_catalog/`, `helpdesk_data/software_catalog.json`, test case G02, G07 | Tra cứu trạng thái phê chuẩn phần mềm (approved, requires_approval, prohibited) | Tự động gắn security_warning và hướng dẫn xử lý nghiêm cấm đối với phần mềm độc hại / torrent / VPN ngoài |
| Bonus: inspect_meeting_room | `tools/inspect_meeting_room/`, `helpdesk_data/meeting_rooms.json`, test case G03, G06 | Tra cứu danh mục màn hình, camera, micro và sự cố AV của các phòng họp | Không lưu trữ hoặc tiết lộ nội dung cuộc họp riêng tư hay video feed nội bộ |
| Bonus: lookup_ticket_status | `tools/lookup_ticket_status/`, `helpdesk_data/tickets.json`, test case G04 | Tra cứu tiến độ và người phụ trách ticket từ local store `tickets/` và historical records | Guardrail chặn path traversal (`../`), tự động kiểm tra và che giấu credential `[REDACTED_CREDENTIAL]` |

## B6. Safety review

- Agent có bao giờ tự đoán asset ID hoặc employee ID không?
- Trace/ticket có chứa password, MFA code, token hay dữ liệu thật không?
- Ticket chỉ được tạo sau xác nhận rõ chưa?
- Tool result error nào cần review thủ công?

## B7. Technical reflection

- Fix nào thuộc `system_prompt.md`?
- Fix nào thuộc `tools.yaml`?
- Failure nào không thể chỉ nhìn automatic score?
- Nếu có thêm một vòng, nhóm sẽ thử hypothesis nào?

# PHẦN C — Checkout trước khi nộp

Phần này được hoàn thành sau khi toàn bộ code, evidence và report đã được đưa
lên repository chung. Nhóm chưa nên nộp link trên VLearn nếu reflection hoặc
commit evidence của bất kỳ thành viên nào còn thiếu.

## C1. Reflection chung của nhóm

Các thành viên thảo luận và viết một reflection chung. Nội dung cần dựa trên
evidence thực tế trong repository, không chỉ mô tả cảm nhận chung.

- Mục tiêu nào của nhóm đã hoàn thành? Dẫn đến artifact hoặc run tương ứng.
- Hypothesis hoặc thay đổi nào tạo ra cải thiện rõ nhất?
- Failure quan trọng nào vẫn chưa xử lý được hoàn toàn?
- Nhóm đã phân chia, review và tích hợp công việc như thế nào?
- Nếu có thêm một vòng, nhóm sẽ ưu tiên thay đổi và kiểm chứng điều gì?

**Reflection chung của nhóm:**

> Viết reflection tại đây và dẫn link/path đến evidence liên quan.

## C2. Self-reflection của từng thành viên

Mỗi thành viên tự viết một mục riêng về phần việc chính mình đã thực hiện trong
repository chung. Không viết thay hoặc gộp nhiều thành viên vào một câu trả lời.
Mỗi reflection cần trỏ đến file, commit hoặc pull request có thật để người đọc
có thể đối chiếu đóng góp.

Sao chép mẫu dưới đây cho từng thành viên:

### Họ tên — MSSV

- **Vai trò/phần việc được nhận:**
- **Những gì tôi đã thay đổi trong repo chung:**
- **File hoặc artifact liên quan:**
- **Commit hash hoặc pull request:**
- **Một quyết định kỹ thuật tôi đã đưa ra và lý do:**
- **Khó khăn tôi gặp và cách tôi xử lý:**
- **Điều tôi học được từ phần việc này:**
- **Nếu làm lại, tôi sẽ cải thiện điều gì:**

Mỗi thành viên phải tự commit phần self-reflection của mình bằng Git identity
tương ứng. Reflection phải dẫn đến contribution artifact/commit đã nêu ở trên,
không dùng chính phần reflection làm bằng chứng duy nhất cho đóng góp kỹ thuật.

## C3. Final checkout

Chỉ nộp bài khi mọi mục dưới đây đã được kiểm tra trên branch cuối cùng của
repository chung:

- [ ] `TEAMMATES.md` có đủ họ tên, MSSV, GitHub username và vai trò.
- [ ] Mỗi thành viên có ít nhất một commit trong lịch sử branch nộp bài.
- [ ] Phần reflection chung của nhóm đã hoàn thành và có evidence.
- [ ] Mỗi thành viên đã tự viết và commit self-reflection của mình.
- [ ] `system_prompt.md`, `tools.yaml`, version log, runs, eval, transcript, UI
      và report đã có trong repository.
- [ ] Không có `.env`, API key, token, dữ liệu thật, cache hoặc generated ticket.
- [ ] Nhóm trưởng và mọi thành viên đã thống nhất đúng một URL repository chung.
- [ ] Nhóm trưởng và mọi thành viên sẽ nộp cùng URL đó trên VLearn.

**URL repository chung dùng để nộp:**

> URL:
