<%!import com.cn.filters.str.str_filters as str_filters%>package ${ packagePath }

% for remotePackage in remotePackages:
import ${ remotePackage }

% endfor
public class ${ className } {
    % for propertyMap in properties:
    ${ propertyMap['authority'] } ${ propertyMap['type'] } ${ propertyMap['name'] } = ${ propertyMap['defaultValue'] };
    % endfor
    % for methodMap in beanMethods:

    ${ methodMap['authority'] } ${ methodMap['returnType'] } get${ methodMap['propertyName'] | str_filters.first_char_upper }() {
        return ${ methodMap['propertyName'] };
    }

    ${ methodMap['authority'] } void set${ methodMap['propertyName'] | str_filters.first_char_upper }(${ methodMap['returnType'] } ${ methodMap['propertyName'] }) {
        this.${ methodMap['propertyName'] } = ${ methodMap['propertyName'] };
    }
    % endfor
}