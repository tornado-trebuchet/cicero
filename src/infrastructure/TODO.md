# Infrastructure Layer TODOs

## Critical Issues Requiring Domain Clarification

### 1. Period Entity vs ValueObject Mismatch
**Status**: ✅ RESOLVED - Infrastructure Aligned with Domain
- **Solution**: Period remains ValueObject as domain dictates - embedded as JSONB in ProtocolORM
- **Changes Made**:
  - Removed `period_id` foreign key from ProtocolORM
  - Added `period_data` JSONB field to ProtocolORM for embedded Period
  - Removed PeriodORM relationship from ProtocolORM
  - Institution already had `periods_data` JSONB for Period collections
- **Files Fixed**: 
  - `infrastructure/orm/text/orm_protocol.py` ✅

### 2. Speaker Aggregate Design Issues  
**Status**: ✅ RESOLVED - Domain Requirements Met
- **Solution**: Added `country_id` to SpeakerORM for proper Speaker reconstruction
- **Changes Made**:
  - Added `country_id` field to SpeakerORM with foreign key to countries
  - Added `country` relationship to SpeakerORM
  - Added `speakers` back-reference to CountryORM
  - Added country index to SpeakerORM
- **Files Fixed**:
  - `infrastructure/orm/context/orm_speaker.py` ✅
  - `infrastructure/orm/context/orm_country.py` ✅

## Mapper Layer Fixes Needed

### 3. SpeechMapper Domain Alignment
**Status**: 🟡 PARTIALLY FIXED - Needs Repository Update
- **Issue**: Fixed to use `speaker_id` but repository still needs updating
- **Action**: Update speech repository to use new mapper signature
- **Files**: `infrastructure/repository/pgsql/rep_speech.py`

### 4. Protocol Text Storage Missing
**Status**: ✅ RESOLVED - ProtocolText ValueObject Storage Added
- **Solution**: Added `protocol_text` field to ProtocolORM for ProtocolText ValueObject storage
- **Changes Made**:
  - Added `protocol_text: Mapped[Optional[str]]` field to ProtocolORM
- **Files Fixed**: `infrastructure/orm/text/orm_protocol.py` ✅

### 5. Speaker Party Enum Reconstruction
**Status**: 🟡 COMPLEX DESIGN ISSUE
- **Issue**: Party enums require country context but mapper doesn't have access
- **Current**: Mapper sets party=None, repository should handle
- **Solution**: Repository layer needs to handle party enum conversion with country context
- **Files**: `infrastructure/repository/pgsql/rep_speaker.py` (when created)

## Repository Layer Improvements

### 6. Missing Speaker Repository
**Status**: 🔴 MISSING COMPONENT
- **Need**: Create SpeakerRepository following DDD patterns
- **Requirements**:
  - Handle party enum conversion with country context
  - Manage speaker aggregate boundaries properly
  - Implement proper speaker-speech relationship loading
- **Files**: Create `infrastructure/repository/pgsql/rep_speaker.py`

### 7. Protocol Repository Issues
**Status**: 🟡 NEEDS REVIEW
- **Issue**: May have similar aggregate boundary violations as fixed repositories
- **Action**: Review and fix Protocol repository following same DDD patterns
- **Files**: `infrastructure/repository/pgsql/rep_protocol.py` (if exists)

## ORM Layer Enhancements

### 8. Missing ORM Fields
**Status**: ✅ RESOLVED - All Domain Data Can Be Persisted
- **Added Fields**:
  - ProtocolORM.protocol_text ✅ (for ProtocolText ValueObject storage)
  - SpeakerORM.country_id ✅ (for proper Speaker reconstruction)
- **Impact**: Domain data can now be properly persisted and reconstructed

### 9. Period Table Cleanup
**Status**: ✅ COMPLETE - Period Properly Implemented as ValueObject
- **Solution**: Period remains ValueObject as domain requires
- **Implementation**:
  - Period embedded as JSONB in ProtocolORM (`period_data` field)
  - Period collections stored as JSONB in InstitutionORM (`periods_data` field)
  - ✅ Removed PeriodORM table (period has no identity)
- **Result**: Infrastructure now fully respects Period as ValueObject

## Import Standardization

### 10. Remaining Import Inconsistencies
**Status**: 🟢 MOSTLY FIXED - Minor Cleanup
- **Issue**: Some files still have mixed `domain.` vs `src.domain.` imports
- **Action**: Systematic cleanup of remaining files
- **Priority**: Low (doesn't break functionality)

## Testing Implications

### 11. Repository Tests Need Updates
**Status**: 🟡 BROKEN TESTS EXPECTED
- **Issue**: Repository changes likely broke existing tests
- **Action**: Update tests to match new DDD-compliant repositories
- **Files**: `tests/infrastructure/repository/`

### 12. Mapper Tests Need Creation
**Status**: 🔴 MISSING TEST COVERAGE
- **Issue**: Fixed mappers need comprehensive tests
- **Priority**: High (mappers are critical translation layer)
- **Files**: Create `tests/infrastructure/mappers/`

## Performance Considerations

### 13. N+1 Query Prevention
**Status**: 🟡 NEEDS MONITORING
- **Issue**: Repository changes may have introduced N+1 queries
- **Action**: Review query patterns and add proper eager loading where needed
- **Files**: All repository files

### 14. JSONB Indexing Strategy
**Status**: 🟡 OPTIMIZATION OPPORTUNITY
- **Issue**: JSONB fields (periods, metadata) may need indexing for performance
- **Action**: Analyze query patterns and add appropriate JSONB indexes
- **Files**: Database migration files

## Migration Strategy

### 15. Database Schema Changes Required
**Status**: � PARTIALLY COMPLETE - Core ORM Changes Done
- **Completed Changes**:
  - ✅ Added protocol_text to protocols table
  - ✅ Added country_id to speakers table  
  - ✅ Added period_data JSONB to protocols table
  - ✅ Removed period_id foreign key from protocols table
- **Remaining**: Database migration scripts needed for existing data
- **Risk**: Data migration required for existing data

---

## Priority Matrix

### 🔴 CRITICAL (Blocks Development)
1. ~~Period Entity vs ValueObject decision~~ ✅ RESOLVED
2. ~~Speaker aggregate design~~ ✅ RESOLVED 
3. ~~Protocol text storage~~ ✅ RESOLVED
4. Missing Speaker repository (#6) 
5. Protocol repository review (#7)

### 🟡 HIGH (Impacts Quality)
5. Speaker party enum handling (#5)
6. Protocol repository review (#7)
7. ORM field additions (#8)
8. Repository tests (#11)

### 🟢 MEDIUM (Nice to Have)
9. Import cleanup (#10)
10. Mapper tests (#12)
11. Performance monitoring (#13, #14)

### 🔵 LOW (Future Enhancement)
12. Database optimization (#15)

---

*Last Updated: July 2, 2025*
*Next Review: After resolving critical domain design decisions*
