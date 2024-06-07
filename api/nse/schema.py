from datetime import datetime
from pydantic import BaseModel, validator
from typing import List, Optional, Union


class BaseSchema(BaseModel):
    @validator('*')
    def strip_and_convert_none(cls, v):
        if isinstance(v, str):
            v = v.strip()
            if v.lower() in ['na', 'nan', '', 'null', "-"]:
                return None
            return v
        else:
            return v
    
    @validator('*')
    def convert_to_datetime(cls, v):
        date_formats = [
            "%d-%b-%Y",    # 25-May-2023
            "%Y-%m-%d",    # 2023-05-25
            "%m/%d/%Y",    # 05/25/2023
            "%m-%d-%Y",    # 05-25-2023
            "%b %d, %Y",   # May 25, 2023
            "%B %d, %Y",   # May 25, 2023 (full month name)
            "%d %b %Y",    # 25 May 2023
            "%d %B %Y",    # 25 May 2023 (full month name)
            "%Y/%m/%d",    # 2023/05/25
            "%Y%m%d",      # 20230525
            "%d/%m/%Y",    # 25/05/2023
            "%d-%m-%Y",    # 25-05-2023
            "%Y.%m.%d",    # 2023.05.25
            "%d.%m.%Y",    # 25.05.2023
            "%m.%d.%Y",    # 05.25.2023
            "%m.%d.%y",    # 05.25.23
            "%m-%d-%y",    # 05-25-23
            "%d-%m-%y",    # 25-05-23
            "%Y%m%d%H%M%S",  # 20230525120000
            "%Y-%m-%dT%H:%M:%S",  # 2023-05-25T12:00:00
            "%Y-%m-%d %H:%M:%S",  # 2023-05-25 12:00:00
            "%Y-%m-%d %H:%M",     # 2023-05-25 12:00
            "%Y-%m-%d %I:%M:%S %p",  # 2023-05-25 12:00:00 PM
            "%Y-%m-%d %I:%M %p",     # 2023-05-25 12:00 PM
            "%d.%m.%y",    # 25.05.23 (with 2-digit year)
            "%m/%d/%y",    # 05/25/23 (with 2-digit year)
            "%m-%d-%y",    # 05-25-23 (with 2-digit year)
            "%d-%m-%y",    # 25-05-23 (with 2-digit year)
            # Add more date formats as needed
        ]
        if isinstance(v, str):
            for date_format in date_formats:
                try:
                    date_obj = datetime.strptime(v, date_format)
                    return date_obj.strftime("%Y-%m-%d")
                except ValueError:
                    pass
        return v


class EquityInfoSchema(BaseSchema):
    symbol: Optional[str]
    nameOfCompany: Optional[str]
    series: Optional[str]
    dateOfListing: Optional[str]
    isinNumber: Optional[str]
    faceValue: Optional[int]
    marketLot: Optional[int]
    paidUpValue: Optional[int]


class CompanyInfoSchema(BaseSchema):
    symbol: Optional[str]
    companyName: Optional[str]
    activeSeries: Optional[List[Optional[str]]]
    debtSeries: Optional[List[Optional[str]]]
    isFNOSec: Optional[bool]
    isCASec: Optional[bool]
    isSLBSec: Optional[bool]
    isDebtSec: Optional[bool]
    isSuspended: Optional[bool]
    tempSuspendedSeries: Optional[List[Optional[str]]]
    isETFSec: Optional[bool]
    isDelisted: Optional[bool]
    isin: Optional[str] = None
    isMunicipalBond: Optional[bool]
    isTop10: Optional[bool]
    identifier: Optional[str]


class IndustryInfoSchema(BaseSchema):
    macro: Optional[str]
    sector: Optional[str]
    industry: Optional[str]
    basicIndustry: Optional[str]


class MetadataSchema(BaseSchema):
    series: Optional[str]
    symbol: Optional[str]
    isin: Optional[str]
    status: Optional[str]
    listingDate: Optional[str]
    industry: Optional[str]
    lastUpdateTime: Optional[str]
    pdSectorPe: Optional[float]
    pdSymbolPe: Optional[float]
    pdSectorInd: Optional[str]

    @validator('pdSectorPe', 'pdSymbolPe', 'pdSectorInd', pre=True)
    def convert_na_to_none(cls, v):
        if v == 'NA':
            return None
        return v

class SurveillanceInfo(BaseSchema):
    surv: Optional[str]
    desc: Optional[str]

class SecurityInfoSchema(BaseSchema):
    boardStatus: Optional[str]
    tradingStatus: Optional[str]
    tradingSegment: Optional[str]
    sessionNo: Optional[Union[str, int]]
    slb: Optional[str]
    classOfShare: Optional[str]
    derivatives: Optional[str]
    surveillance: Optional[SurveillanceInfo]
    faceValue: Optional[int]
    issuedSize: Optional[int]

class IntraDayHighLow(BaseSchema):
    min: Optional[float]
    max: Optional[float]
    value: Optional[float]


class WeekHighLow(BaseSchema):
    min: Optional[float]
    minDate: Optional[str]
    max: Optional[float]
    maxDate: Optional[str]
    value: Optional[float]


class PriceInfoSchema(BaseSchema):
    lastPrice: Optional[float]
    change: Optional[float]
    pChange: Optional[float]
    previousClose: Optional[float]
    open: Optional[float]
    close: Optional[float]
    vwap: Optional[float]
    lowerCP: Optional[str]
    upperCP: Optional[str]
    pPriceBand: Optional[str]
    basePrice: Optional[float]
    intraDayHighLow: Optional[IntraDayHighLow]
    weekHighLow: Optional[WeekHighLow]
    iNavValue: Optional[float]
    checkINAV: Optional[bool]
