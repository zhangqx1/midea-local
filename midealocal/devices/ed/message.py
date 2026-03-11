"""Midea local ED message."""

from enum import IntEnum

from midealocal.const import DeviceType
from midealocal.message import (
    ListTypes,
    MessageBody,
    MessageRequest,
    MessageResponse,
    MessageType,
)


class Attributes(IntEnum):
    """Attributes."""

    CHILD_LOCK = 0x000
    LIFE = 0x10
    TDS = 0x013
    WATER_CONSUMPTION = 0x011


class NewSetTags(IntEnum):
    """New set tags.

    控制命令的参数标签，对应 Lua 脚本中 setbytes(item1, item2, ...) 的编码方式：
    param = item2 << 8 | item1
    例如 power: setbytes(0x00, 0x01, ...) → 0x01 << 8 | 0x00 = 0x0100
    """

    power = 0x0100
    lock = 0x0201
    # 加热开关控制，对应 Lua: setbytes(0x00, 0x04, value, 0x00, 0x00)
    # param = 0x04 << 8 | 0x00 = 0x0400
    heat = 0x0400


class EDNewSetParamPack:
    """ED new set parameter pack."""

    @staticmethod
    def pack(param: int, value: int, addition: int = 0) -> bytearray:
        """Pack parameter."""
        return bytearray(
            [param & 0xFF, param >> 8, value, addition & 0xFF, addition >> 8],
        )


class MessageEDBase(MessageRequest):
    """ED message base."""

    def __init__(
        self,
        protocol_version: int,
        message_type: MessageType,
        body_type: ListTypes = ListTypes.X00,
    ) -> None:
        """Initialize ED message base."""
        super().__init__(
            device_type=DeviceType.ED,
            protocol_version=protocol_version,
            message_type=message_type,
            body_type=body_type,
        )

    @property
    def _body(self) -> bytearray:
        raise NotImplementedError


class MessageQuery(MessageEDBase):
    """ED message query."""

    def __init__(
        self,
        protocol_version: int,
        body_type: ListTypes = ListTypes.X00,
    ) -> None:
        """Initialize ED message query."""
        super().__init__(
            protocol_version=protocol_version,
            message_type=MessageType.query,
            body_type=body_type,
        )

    @property
    def _body(self) -> bytearray:
        return bytearray([0x01])


class MessageQuery01(MessageEDBase):
    """ED message query01."""

    def __init__(
        self,
        protocol_version: int,
        body_type: ListTypes = ListTypes.X01,
    ) -> None:
        """Initialize ED message query01."""
        super().__init__(
            protocol_version=protocol_version,
            message_type=MessageType.query,
            body_type=body_type,
        )

    @property
    def _body(self) -> bytearray:
        return bytearray([0x01])


class MessageQuery03(MessageEDBase):
    """ED message query03."""

    def __init__(
        self,
        protocol_version: int,
        body_type: ListTypes = ListTypes.X03,
    ) -> None:
        """Initialize ED message query03."""
        super().__init__(
            protocol_version=protocol_version,
            message_type=MessageType.query,
            body_type=body_type,
        )

    @property
    def _body(self) -> bytearray:
        return bytearray([0x01])


class MessageQuery04(MessageEDBase):
    """ED message query04."""

    def __init__(
        self,
        protocol_version: int,
        body_type: ListTypes = ListTypes.X04,
    ) -> None:
        """Initialize ED message query04."""
        super().__init__(
            protocol_version=protocol_version,
            message_type=MessageType.query,
            body_type=body_type,
        )

    @property
    def _body(self) -> bytearray:
        return bytearray([0x01])


class MessageQuery05(MessageEDBase):
    """ED message query05."""

    def __init__(
        self,
        protocol_version: int,
        body_type: ListTypes = ListTypes.X05,
    ) -> None:
        """Initialize ED message query05."""
        super().__init__(
            protocol_version=protocol_version,
            message_type=MessageType.query,
            body_type=body_type,
        )

    @property
    def _body(self) -> bytearray:
        return bytearray([0x01])


class MessageQuery06(MessageEDBase):
    """ED message query06."""

    def __init__(
        self,
        protocol_version: int,
        body_type: ListTypes = ListTypes.X06,
    ) -> None:
        """Initialize ED message query06."""
        super().__init__(
            protocol_version=protocol_version,
            message_type=MessageType.query,
            body_type=body_type,
        )

    @property
    def _body(self) -> bytearray:
        return bytearray([0x01])


class MessageQuery07(MessageEDBase):
    """ED message query07."""

    def __init__(
        self,
        protocol_version: int,
        body_type: ListTypes = ListTypes.X07,
    ) -> None:
        """Initialize ED message query07."""
        super().__init__(
            protocol_version=protocol_version,
            message_type=MessageType.query,
            body_type=body_type,
        )

    @property
    def _body(self) -> bytearray:
        return bytearray([0x01])


class MessageQueryFF(MessageEDBase):
    """ED message queryFF."""

    def __init__(
        self,
        protocol_version: int,
        body_type: ListTypes = ListTypes.FF,
    ) -> None:
        """Initialize ED message queryFF."""
        super().__init__(
            protocol_version=protocol_version,
            message_type=MessageType.query,
            body_type=body_type,
        )

    @property
    def _body(self) -> bytearray:
        return bytearray([0x01])


class MessageNewSet(MessageEDBase):
    """ED message new set."""

    def __init__(self, protocol_version: int) -> None:
        """Initialize ED message new set."""
        super().__init__(
            protocol_version=protocol_version,
            message_type=MessageType.set,
            body_type=ListTypes.X15,
        )
        self.power: bool | None = None
        self.lock: bool | None = None
        # 加热开关，True=开启加热, False=关闭加热
        self.heat: bool | None = None

    @property
    def _body(self) -> bytearray:
        pack_count = 0
        payload = bytearray([0x01, 0x00])
        if self.power is not None:
            pack_count += 1
            payload.extend(
                EDNewSetParamPack.pack(
                    param=NewSetTags.power,  # power
                    value=0x01 if self.power else 0x00,
                ),
            )
        if self.lock is not None:
            pack_count += 1
            payload.extend(
                EDNewSetParamPack.pack(
                    param=NewSetTags.lock,  # lock
                    value=0x01 if self.lock else 0x00,
                ),
            )
        # 加热开关控制，对应 Lua: setbytes(0x00, 0x04, 0x01/0x00, 0x00, 0x00)
        if self.heat is not None:
            pack_count += 1
            payload.extend(
                EDNewSetParamPack.pack(
                    param=NewSetTags.heat,  # heat
                    value=0x01 if self.heat else 0x00,
                ),
            )
        payload[1] = pack_count
        return payload


class MessageOldSet(MessageEDBase):
    """ED message old set."""

    def __init__(self, protocol_version: int) -> None:
        """Initialize ED message old set."""
        super().__init__(
            protocol_version=protocol_version,
            message_type=MessageType.set,
        )

    @property
    def body(self) -> bytearray:
        """ED message old set body."""
        return bytearray([])

    @property
    def _body(self) -> bytearray:
        return bytearray([])


class EDMessageBody01(MessageBody):
    """ED message body 01.

    对应 Lua 脚本中 (byte9==0x03, byte10==0x01) 的解析分支。
    Lua 字节编号与 body[] 索引对应关系: body[N] = Lua byte(N+10)

    body[2] (Lua byte12) 各 bit 含义:
        bit0 (0x01): power       - 电源开关
        bit1 (0x02): heat        - 加热开关
        bit2 (0x04): heat_status - 加热运行状态(只读)
        bit3 (0x08): cool        - 制冷开关
        bit4 (0x10): cool_status - 制冷运行状态
        bit5 (0x20): bubble      - 气泡洗开关
        bit6 (0x40): bubble_status - 气泡洗运行状态
    body[10] (Lua byte20): heat_temperature - 加热目标温度
    body[11] (Lua byte21): cool_temperature - 制冷目标温度
    """

    def __init__(self, body: bytearray) -> None:
        """Initialize ED message body 01."""
        super().__init__(body)
        self.power = (body[2] & 0x01) > 0
        # body[2] bit1: 加热开关(用户是否开启了加热)
        self.heat = (body[2] & 0x02) > 0
        # body[2] bit2: 加热运行状态(设备当前是否正在加热, 只读)
        self.heat_status = (body[2] & 0x04) > 0
        self.water_consumption = body[7] + (body[8] << 8)
        # body[10] (Lua byte20): 加热目标温度
        self.heat_temperature = body[10]
        self.in_tds = body[36] + (body[37] << 8)
        self.out_tds = body[38] + (body[39] << 8)
        self.child_lock = body[15] > 0
        self.filter1 = round((body[25] + (body[26] << 8)) / 24)
        self.filter2 = round((body[27] + (body[28] << 8)) / 24)
        self.filter3 = round((body[29] + (body[30] << 8)) / 24)
        self.life1 = body[16]
        self.life2 = body[17]
        self.life3 = body[18]


class EDMessageBody03(MessageBody):
    """ED message body 03."""

    def __init__(self, body: bytearray) -> None:
        """Initialize ED message body 03."""
        super().__init__(body)
        self.power = (body[51] & 0x01) > 0
        self.child_lock = (body[51] & 0x08) > 0
        self.water_consumption = body[20] + (body[21] << 8)
        self.life1 = body[22]
        self.life2 = body[23]
        self.life3 = body[24]
        self.in_tds = body[27] + (body[28] << 8)
        self.out_tds = body[29] + (body[30] << 8)


class EDMessageBody05(MessageBody):
    """ED message body 05."""

    def __init__(self, body: bytearray) -> None:
        """Initialize ED message body 05."""
        super().__init__(body)
        self.power = (body[51] & 0x01) > 0
        self.child_lock = (body[51] & 0x08) > 0
        self.water_consumption = body[20] + (body[21] << 8)


class EDMessageBody06(MessageBody):
    """ED message body 06."""

    def __init__(self, body: bytearray) -> None:
        """Initialize ED message body 06."""
        super().__init__(body)
        self.power = (body[51] & 0x01) > 0
        self.child_lock = (body[51] & 0x08) > 0
        self.water_consumption = body[25] + (body[26] << 8)


class EDMessageBody07(MessageBody):
    """ED message body 07."""

    def __init__(self, body: bytearray) -> None:
        """Initialize ED message body 07."""
        super().__init__(body)
        self.water_consumption = (body[21] << 8) + body[20]
        self.power = (body[51] & 0x01) > 0
        self.child_lock = (body[51] & 0x08) > 0


class EDMessageBodyFF(MessageBody):
    """ED message body FF."""

    def __init__(self, body: bytearray) -> None:
        """Initialize ED message body FF."""
        super().__init__(body)
        data_offset = 2
        while True:
            length = (body[data_offset + 2] >> 4) + 2
            attr = ((body[data_offset + 2] % 16) << 8) + body[data_offset + 1]
            if attr == Attributes.CHILD_LOCK:
                self.child_lock = (body[data_offset + 5] & 0x01) > 0
                self.power = (body[data_offset + 6] & 0x01) > 0
            elif attr == Attributes.WATER_CONSUMPTION:
                self.water_consumption = (
                    float(
                        body[data_offset + 3]
                        + (body[data_offset + 4] << 8)
                        + (body[data_offset + 5] << 16)
                        + (body[data_offset + 6] << 24),
                    )
                    / 1000
                )
            elif attr == Attributes.TDS:
                self.in_tds = body[data_offset + 3] + (body[data_offset + 4] << 8)
                self.out_tds = body[data_offset + 5] + (body[data_offset + 6] << 8)
            elif attr == Attributes.LIFE:
                self.life1 = body[data_offset + 3]
                self.life2 = body[data_offset + 4]
                self.life3 = body[data_offset + 5]
            # fix index out of range error
            if data_offset + length + 6 > len(body):
                break
            data_offset += length


class EDMessageBody15(MessageBody):
    """ED message body 15 (set command response).

    Set 命令(body_type=0x15)的响应体解析。
    响应格式与发送格式一致：
        body[0] = 0x15 (body_type, 已被 MessageBody 解析)
        body[1] = pack_count (参数个数)
        body[2] = 0x00
        然后每 5 字节一组：[item1, item2, value, addition_lo, addition_hi]
        param = item2 << 8 | item1

    从响应中提取各控制属性的确认值，避免使用 EDMessageBodyFF 错误解析。
    """

    def __init__(self, body: bytearray) -> None:
        """Initialize ED message body 15."""
        super().__init__(body)
        if len(body) < 3:  # noqa: PLR2004
            return
        pack_count = body[1]
        offset = 3  # skip body_type(body[0]), pack_count(body[1]), reserved(body[2])
        for _ in range(pack_count):
            if offset + 5 > len(body):
                break
            param = body[offset + 1] << 8 | body[offset]
            value = body[offset + 2]
            if param == NewSetTags.power:
                self.power = value > 0
            elif param == NewSetTags.lock:
                self.child_lock = value > 0
            elif param == NewSetTags.heat:
                self.heat = value > 0
            offset += 5


class MessageEDResponse(MessageResponse):
    """ED message response."""

    def __init__(self, message: bytes) -> None:
        """Initialize ED message response."""
        super().__init__(bytearray(message))
        if self._message_type in [
            MessageType.set,
            MessageType.query,
            MessageType.notify1,
        ]:
            self.device_class = self._body_type
            # Lua 脚本中只解析 query(0x03) 和 notify(0x04) 的响应，
            # set(0x02) 响应不解析（美的美居也不依赖 set 响应更新状态）。
            # 因此 set 响应不应进入任何 body 解析分支，
            # 避免 EDMessageBodyFF 错误解析 0x15 格式数据导致属性被覆盖。
            if self._message_type != MessageType.set:
                if self._body_type in [ListTypes.X00, ListTypes.FF]:
                    self.set_body(EDMessageBodyFF(super().body))
                if self.body_type == ListTypes.X01:
                    self.set_body(EDMessageBody01(super().body))
                elif self.body_type in [ListTypes.X03, ListTypes.X04]:
                    self.set_body(EDMessageBody03(super().body))
                elif self.body_type == ListTypes.X05:
                    self.set_body(EDMessageBody05(super().body))
                elif self.body_type == ListTypes.X06:
                    self.set_body(EDMessageBody06(super().body))
                elif self.body_type == ListTypes.X07:
                    self.set_body(EDMessageBody07(super().body))
        self.set_attr()
